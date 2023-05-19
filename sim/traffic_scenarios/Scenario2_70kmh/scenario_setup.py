import glob
import os
import sys
import pandas as pd
import xml.etree.ElementTree as ET
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla
import argparse
import random
import time
import logging
from datetime import datetime, date
from typing import Any
from multiprocessing import Process, Queue
# ===============================================
def current_time():
  # Current Time
  now = datetime.now()
  Current_time = now.strftime("%Y-%m-%d %H.%M.%S")
  return Current_time
# read experiment Number
root = ET.parse('experiment_data.xml').getroot()
X = root.find('data')
experiment_nr = int(root.find("ex_nr").text)
def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2099,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '--safe',
        action='store_true',
        help='avoid spawning vehicles prone to accidents')
    argparser.add_argument(
        '-f', '--recorder_filename',
        metavar='F',
        default="test1.log",
        help='recorder filename (test1.log)')
    argparser.add_argument(
        '-t', '--recorder_time',
        metavar='T',
        default=0,
        type=int,
        help='recorder duration (auto-stop)')
    argparser.add_argument(
        '--tm_port',
        metavar='P',
        default=8000,
        type=int,
        help='Port to communicate with TM (default: 8000)')

    args = argparser.parse_args()
    actor_list = []
    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(20.0)
        world = client.load_world('Town06_Opt')
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)
        blueprints = world.get_blueprint_library().filter('vehicle.*')
        tm = client.get_trafficmanager(args.tm_port)
        tm.set_random_device_seed(12)
        client.start_recorder("/replace with your own system path where you want to store data/carla_log/Ex_{}_record_{}.log".format(experiment_nr, current_time()), True)
        # --------------
        # Locations to spawn
        Lead_vehicle_location=  carla.Transform(carla.Location(x=25.379946, y=244.533249, z=0.300000), carla.Rotation(pitch=0.000000, yaw=0.019546, roll=0.000000))
        # --------------
        # Vehicle to spawn
        Lead_vehicle_type = world.get_blueprint_library().find('vehicle.tesla.cybertruck')
        npc = world.try_spawn_actor(Lead_vehicle_type, Lead_vehicle_location)
        if npc is not None:
          actor_list.append(npc)
          print('created %s' % npc.type_id)

        # =========================================================================
        transform = carla.Transform(carla.Location(x=22.379946, y=244.533249, z=0.300000),
                             carla.Rotation(pitch=0.000000, yaw=0.019546, roll=0.000000))
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(transform.location + carla.Location(z=100),
                                                carla.Rotation(pitch=-90)))
        if (args.recorder_time > 0):
            time.sleep(args.recorder_time)
        else:
            while True:
                world.wait_for_tick()
                world_snapshot = world.get_snapshot()  # Retrieve a snapshot of the world at current frame.
                tt = world_snapshot.timestamp.elapsed_seconds
                if tt >2.0 and tt < 15.00:
                  actor_list[0].apply_control(carla.VehicleControl(throttle=0.54, brake=0, steer=0))
                elif tt >15.0 and tt < 20.00:
                  actor_list[0].apply_control(carla.VehicleControl(throttle=0.493, brake=0, steer=0))
                elif tt >= 20.0 and tt < 50.55:
                  actor_list[0].disable_constant_velocity()
                  actor_list[0].apply_control(carla.VehicleControl(throttle=0, brake=0.3, steer=0))

    finally:
        print('\ndestroying %d actors' % len(actor_list))
        client.apply_batch_sync([carla.command.DestroyActor(x) for x in actor_list])
        print("Stop recording")
        client.stop_recorder()

if __name__ == '__main__':
    try:
        time.sleep(5)
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')

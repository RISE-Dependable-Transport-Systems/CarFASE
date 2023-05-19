import csv
from datetime import datetime, date, time
import pandas as pd
import glob
import  os
from timeit import default_timer as timer
start_time = timer()
# logged data file name for attack injection campaign
campaign_log_file = 'CarFASE Fault Injection Campaign Log _*.csv'
# Reads all log files with extension of fcd.xml and lists them
file_list = sorted(glob.glob("output/*Sensor_data_*.log"), key=os.path.getmtime)
print('file list: ', file_list)
Ex_nr = 0
Lane_invasion_LIST = []
Lane_invasion_time_LIST = []
Collision_LIST = []
Collision_time_LIST = []
#==================================================================================#
#                      Read log data for each experiment                           #
#==================================================================================#
for file_i in file_list:
  file = open(file_i, "r")
  Ex_nr+=1
  print("Experiment_Nr = ", Ex_nr, "***************\n\n")
  lane_invasion_event = []
  lane_invasion_event_time = []
  collision_event = []
  collision_event_time = []
  for line in file.readlines():
    if "CollisionEvent" in line:
      a, b, c, d = map(str.strip, line.split(","))
      collision_event.append('Yes')
      collision_event_time.append(c)
    # for line in file.readlines():
    elif "LaneInvasionEvent" in line:
      lane_invasion_event.append('Yes')
      a, b, c = map(str.strip, line.split(","))
      c = c.replace(')', '')
      lane_invasion_event_time.append(c)
  if len(lane_invasion_event) > 0:
    Lane_invasion_LIST.append('Yes')
    Lane_invasion_time_LIST.append(lane_invasion_event_time[0])
  else:
    Lane_invasion_LIST.append('No')
    Lane_invasion_time_LIST.append('-')
  if len(collision_event) > 0:
    Collision_LIST.append('Yes')
    Collision_time_LIST.append(collision_event_time[0])
  else:
    Collision_LIST.append('No')
    Collision_time_LIST.append('-')

print('list_L  ', Lane_invasion_LIST)
print('list_L_time  ', Lane_invasion_time_LIST)
print('list_C  ', Collision_LIST)
print('list_C_time  ', Collision_time_LIST)

#==================================================================================#
#                      Read log data for fault campaign                           #
#==================================================================================#

f = open(campaign_log_file, 'r')
readCSV = csv.reader(f)
experiment_nr = []
startTime = []
endTime = []
value = []
next(readCSV)
for row in readCSV:
    experiment_nr.append(int(row[1]))
    startTime.append(float(row[2]))
    endTime.append(float(row[3]))
    value.append(float(row[5]))

#==================================================================================#
#                      Save parsed data as a .csv file                             #
#==================================================================================#
df_7 = pd.DataFrame(
        {
            'Ex ID':                    experiment_nr,
            'Start_time':               startTime,
            'End_time':                 endTime,
            'Injected_value':           value,
            'Lane_invasion_event':      Lane_invasion_LIST,
            'Lane_invasion_event_time': Lane_invasion_time_LIST,
            'Collision_event':          Collision_LIST,
            'Collision_event_time':     Collision_time_LIST
                }
        )
# Current time extraction
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H.%M.%S")
df_7.to_csv("Parsed_Lane_invasion_and_Collision_Data_{}.csv".format(current_time))

print(" It took:  ", timer()-start_time)

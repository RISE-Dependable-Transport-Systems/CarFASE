##############################################################################################
# **************           AutoRun:                                             **************
##############################################################################################
import subprocess
import numpy
from datetime import datetime, date, time
import pandas as pd
import xml.etree.ElementTree as ET

def Auto_run():
  subprocess.run(['xterm', '-e', '/opt/sim/carla-files/openpilot/carla13/CarlaUE4.sh --world-port=2099 -RenderOffScreen & '
                                   '/opt/sim/carla-files/openpilot/tools/sim/launch_openpilot.sh & '
                                  '/opt/sim/carla-files/openpilot/tools/sim/campaign_setup.py & '
                                 '/opt/sim/carla-files/openpilot/tools/sim/bridge.py '])

##############################################################################################
# import 'configure_campaign.xml' file and regenerate "experiment_data.xml" file for each experiment
##############################################################################################
config_data = ET.parse('experiment_data.xml')

# LISTS TO LOG fault INJECTION DATA
LIST_Ex_Nr = []                     # Experiment ID
LIST_Initiation_time = []           # Fault Start/Activation Time
LIST_End_time = []                  # Fault End Time
LIST_Step_number = []               # Number of Experiment in the Selected Fault Activation Period
LIST_Injected_value = []            # Injected Fault Values
LIST_Run_status = []

configurationFile = ET.parse('configure_campaign.xml').getroot()
def config(faultModelName):
  faultModel = configurationFile.find(str(faultModelName))
  faultInitiationStartTime = float(faultModel.get("faultInitiationStartTime"))
  faultInitiationEndTime = float(faultModel.get("faultInitiationEndTime"))
  faultInitiationTimeStep = float(faultModel.get("faultInitiationTimeStep"))
  faultStartValue = float(faultModel.get("faultStartValue"))
  faultEndValue = float(faultModel.get("faultEndValue"))
  faultValueStep = float(faultModel.get("faultValueStep"))
  faultMinDuration = float(faultModel.get("faultMinDuration"))
  faultMaxDuration = float(faultModel.get("faultMaxDuration"))
  faultDurationStep = float(faultModel.get("faultDurationStep"))
  Ex_Nr = 0    # Number of experiment (Ex_Nr)

  for faultInitiationTime in numpy.arange(faultInitiationStartTime, faultInitiationEndTime,
                                           faultInitiationTimeStep):  # This loop defines the target time to inject fault
    faultInitiationTime = round(faultInitiationTime, 2)
    Step_number = 0  # Counts the step of the experiment
    for faultValue in numpy.arange(faultStartValue, faultEndValue,
                                    faultValueStep):  # Injected_value is a faulty value, this loop defines the target range
      faultValue = round(faultValue, 3)
      for faultDuration in numpy.arange(faultMinDuration, faultMaxDuration, faultDurationStep):
        endTime = faultInitiationTime + faultDuration
        Ex_Nr += 1
        Step_number += 1
        LIST_Ex_Nr.append(Ex_Nr)
        LIST_Initiation_time.append(faultInitiationTime)
        LIST_End_time.append(endTime)
        LIST_Step_number.append(Step_number)
        LIST_Injected_value.append(faultValue)
        config_data.find('start_time').text = str(faultInitiationTime)
        config_data.find('end_time').text = str(endTime)
        config_data.find('b_factor').text = str(faultValue)
        config_data.find('noise_type').text = str(faultModelName)
        config_data.find('ex_nr').text = str(Ex_Nr)
        config_data.write('experiment_data.xml')
        print('\n\nEx_Number = ', Ex_Nr,
              '\n\n============================================================='
              '\n================================================================\n')
        try:
          Auto_run()
          LIST_Run_status.append('Successful')
        except Exception as err:
          print("Something went wrong")
          LIST_Run_status.append('Failed')

##############################################################################################
# *************        Function for fault Injection Campaign Data Log         ***************
##############################################################################################
def CarFASE_compaign_data_log():
    # Record data in a csv file
    df = pd.DataFrame(
        {
            'Ex Number': LIST_Ex_Nr,
            'Initiation_time': LIST_Initiation_time,
            'End_time': LIST_End_time,
            'Step_number': LIST_Step_number,
            'Injected_value': LIST_Injected_value,
            'Run_status': LIST_Run_status
        }
    )
    # Current Time
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H.%M.%S")
    df.to_csv("campaign_data/CarFASE Fault Injection Campaign Log _{}.csv".format(current_time))
    print("Current Time =", now)
##############################################################################################
# *************                         Main Function                          ***************
##############################################################################################
if __name__ == "__main__":
  # make sure params are in a good state
  configurationFile = ET.parse('configure_campaign.xml').getroot()
  faultModel = configurationFile.find('Fault_type')
  if faultModel.get("s_p") == 'true':
      faultModelName = "s_p"
      config(faultModelName)
  elif faultModel.get("brightness") == 'true':
      faultModelName = "brightness"
      config(faultModelName)
  else:
      config_data.find('noise_type').text = str('NA')
      config_data.write('experiment_data.xml')
      Auto_run()
      print('Golden-run is finished!!\n\n------------------- Select a fault model in the "configure_campaign.xml" file')
  # Log the fault injection campaign data
  CarFASE_compaign_data_log()


# CarFASE
 CarFASE is a  [Carla](https://carla.org/) based fault and  attack  simulation  engine  that  allows  to  evaluate the behavior of autonomous driving (AD) stacks in the presence of faults and attacks. [OpenPilot](https://comma.ai/openpilot) is one example of AD stacks that is used to intigrate with CarFASE. Below picture shows a high-level architecture of CarFASE along
with its connection to Carla and OpenPilot.

<p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/CarFASE/blob/main/Documentation/pictures/carfase_3.png" width="450" height="300">
</p>
<br/> 
<br/> 
CarFASE consists of three main components, scenario configurator, fault library, and campaign configurator. The scenario configurator is responsible for creating a scenario that consists of a number of vehicles, a certain weather condition, the choice of maps, and the trajectory of vehicles. The fault library contains implementations of different fault models. Finally, the campaign configurator is responsible for applying the chosen fault parameters.


# CarFASE Integration
## Step1: setup of Carla and OpenPilot
Prepare the simulation environment by downloading the below-mentioned versions of Carla and OpenPilot.

Note: CarmFASE is tested on the below-mentioned versions of the simulators:

* [Carla 0.9.13](https://carla.org/2021/11/16/release-0.9.13/)
* [OpenPilot 0.8.12](https://github.com/commaai/openpilot/releases/tag/v0.8.12) 

Follow the instructions provided by the OpenPilot [here](https://github.com/commaai/openpilot/blob/master/tools/README.md) to get the simulation running.

### Integrating CarFASE into the OpenPilot
1. Clone the [CarFASE](https://github.com/RISE-Dependable-Transport-Systems/CarFASE) repository into the sim folder in **../openpilot/tools/sim**
2. Modify the **configure_campaign.xml** file by choosing the fault model and tuning a value for the parameteres such as faultActivationTime, FaultValue, and FaultDuration.
```

<configure>

	<!-- ################################## Fault Model Selection ################################## -->
	<Fault_type 
	brightness="true"
	s_p="false"
	/>
	
	<!-- ############################## Brightness Fault Parameters ############################## -->
	<brightness
	faultInitiationStartTime="20" 	        faultInitiationEndTime="30.1"           faultInitiationTimeStep="0.5" 
	faultStartValue="0" 			faultEndValue="7.51" 			faultValueStep="0.3" 
	faultMinDuration="1" 			faultMaxDuration="10.1" 		faultDurationStep="1" 
	/>
	
	<!-- ################################## S&P Fault Parameters ################################## -->
	<s_p
	faultInitiationStartTime="20" 	        faultInitiationEndTime="30.1"           faultInitiationTimeStep="0.5" 
	faultStartValue="1" 			faultEndValue="7.51" 			faultValueStep="0.3" 
	faultMinDuration="8" 			faultMaxDuration="10.1" 		faultDurationStep="1" 
	/>
	
	
</configure>
```
3. Depending on the selected scenario, move the **bridge.py** and **scenario_setup.py** scripts from traffic_scenarios/.. directory to the sim folder in OpenPilot **../openpilot/tools/sim**

4. Make sure the paths in the scripts are adjusted according to your system directory, for example in below line:
```
client.start_recorder("/replace with your own system's path where you want to store the data/carla_log/Ex_{}_record_{}.log".format(experiment_nr, current_time()), True)
```

5. Run **auto_run.py** script to start the execution of the campaign.

## Result Analysis


## License
CarFASE is an open source tool, the tool is free: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
## Papers

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
2. 
3.  

3. To use the **ComFASE** in the desired part of the code, add below lines to call comfase header file: 
```
#include "veins/base/utils/FindModule.h"
#include "<path to comfase>comfase/src/comfase/attackInjection/Injector.h"
```
Note: the path to the **Injector.h** file can be different depending on your directory.

for **Delay** and **DoS** attacks the following lines are added into the "channelAccess.cc" in source code of the Veins
```
    auto comfase = FindModule<injectorV*>::findGlobalModule();
    if (comfase->DelayAttack){
        std::cout<<"Delay Attack = is TRUE"<<std::endl;
        float correctValue = receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
        return comfase->PropagationDelayAttack(senderModule->getId(), receiverModule->getId(), correctValue);
    }
    else if (comfase->DoSAttack){
        std::cout<<"DoS Attack = is TRUE"<<std::endl;
        float correctValue = receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
        return comfase->DenialOfServiceAttack(senderModule->getId(), receiverModule->getId(), correctValue);
    }
    else{
    // this time-point is used to calculate the distance between sending and receiving host
        return receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
    }
```
3. Update **ned** file of the example that you want to run by adding: 
``` 
import comfase.comfase.injectorVeins.injectorV;
```
and 
```
        comfase: injectorV {
            @display("p=120,50;i=abstract/penguin");
        }
```
4. Update your example **ini** file by adding "attackInjection.ini" as following:
```
include <path to comfase>comfase/src/comfase/injectorVeins/injectorV.ini
```

5. Compile the code to make it ready to run (build all projects in OMNeT++ IDE)

## Option2: ComFASE in cmd environment


-----------------------
# ComFASE Running
## Option1: in OMNeT++ IDE
Configure the attack injection scenario through updating the **attackInjection.ini** file as denoted below, and run the desired example.
```
##########################################################
#                       Attack Start                     #
##########################################################
*.comfase.attackStartTime 	= ${attackStartTime = 12}s
###                      Attack End                       #
###########################################################
*.comfase.attackEndTime 	= ${attackEndTime = 15}s # This is not for DoS attack
#
##          Target Vehicle and Attack Surface             #
###########################################################
*.comfase.attackNode 		= 27
*.comfase.attackActive 	= false
*.comfase.attackOnSender 	= true
*.comfase.attackOnReceiver = false
#
#
##                     Delay Attack                       #
###########################################################
*.comfase.DelayAttack = true
*.comfase.myPDValue 		= ${myPDValue = 0.5}s
#
#
##                      DoS Attack                        #
###########################################################
*.comfase.DoSAttack = false
*.comfase.myPDforDoS		= ${myPDforDoS = 60}s 
```

## Option2: in cmd
A Python script is written to run the ComFASE experiments, before running that you can define your attack injection setup such as target node (target vehicle), attack type (Delay or DoS), and target attack surface (sender, receiver or both):
```
Node=27  		     # NODE/VEHICLE UNDER ATTACK
Activation='true'	     # BOOLEAN FOR ATTACK ACTIVATION
Delay='true'	             # BOOLEAN FOR DELAY
Sender='true'   	     # BOOLEAN FOR TARGET SURFACE FOR SENDER
Receiver='true' 	     # BOOLEAN FOR TARGET SURFACE FOR RECEIVER
for t in numpy.arange(17.0, 21.9, 0.2):  # This loop defines the target time to inject attack
```
## Result Analysis


## License

## Papers

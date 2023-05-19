import pandas as pd
import numpy
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
plt.rcParams['figure.figsize'] = 16,7
import warnings
warnings.filterwarnings('ignore')
#==================================================================================#
#                     Read parsed data for fault campaign                         #
#==================================================================================#
# Data Analysis (DA): pd.read_csv('please correct the address accordingly')
DA = pd.read_csv('Parsed_Lane_invasion_and_Collision_Data_2023-03-08 07.44.42.csv')
DA['FaultDuration'] = round(DA['End_time'] - DA['Start_time'] , 2)
DA['Categories'] = DA['Start_time']
DA['Categories'] = 'NAN'
#==================================================================================#
#    Result classification based on Acceleration Profile and Collisions            #
#==================================================================================#
Non_effective = 0
for index, col in DA.iterrows():
    if DA['Collision_event'][index] == 'Yes':
      DA['Categories'][index] = 'Severe'
    elif DA['Lane_invasion_event'][index] == 'Yes':
        DA['Categories'][index] = 'Benign'
    else:
        DA['Categories'][index] = 'Negligible'
#==================================================================================#
#                                     Categorization                               #
#==================================================================================#
#Change the type
DA.Injected_value  = DA.Injected_value.astype('category')
DA.Start_time = DA.Start_time.astype('category')
DA.Categories = DA.Categories.astype('category')
#==================================================================================#
#              Print: Classified results as Severe, benign, etc.                   #
#==================================================================================#
print('==========================================\n     Classified Results \n==========================================')
print('Total:           ', DA.Categories.count())
print('Severe:          ', DA.Categories[(DA.Categories == "Severe")].count())
print('Benign:          ', DA.Categories[(DA.Categories == "Benign")].count())
print('Negligible:      ', DA.Categories[(DA.Categories == "Negligible")].count())
print('==========================================\n==========================================')
#==================================================================================#
#                 Plot: Fault duration vs Experiment numbers                      #
#==================================================================================#
ATTList = ['Negligible', 'Benign', 'Severe'] #DA.Categories.cat.categories
List = []
Label = []

for name in ATTList:
    List.append(DA[DA.Categories == name].FaultDuration)
    Label.append(name)

sns.set_style('whitegrid')
fig, ax = plt.subplots()
fig.set_size_inches(8.77, 6.2)  # size of A4 paper
sns.set_palette(palette="deep")
plt.hist(List, bins=19, stacked=True, rwidth=2.17,
             label=Label, color={"darkorange", "blue", "darkred"})
plt.xlabel('Fault duration (s)', fontsize=22, color='black')
plt.xticks(fontsize=19)
plt.ylabel('Number of experiments', fontsize=22, color='black')
plt.yticks(fontsize=19)
x_ticks = np.arange(1, 10.1, 1)
plt.xticks(x_ticks)
plt.legend(fontsize=16,  ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.065))
plt.show()
#==================================================================================#
#               Plot: Duration vs Number of Experiments                      #
#==================================================================================#

duration_negligible = []
duration_benign = []
duration_severe = []
numbers_negligible = []
numbers_benign = []
numbers_severe = []
# Change the FaultActivationTimeRange according to the selected traffic scenario such as "Sinusoidal", "Braking"
for faultDuration in numpy.arange(1, 10.1, 1):
    faultDuration = round(faultDuration, 2)
    duration_negligible.append(faultDuration)
    numbers_negligible.append(DA.FaultDuration[(DA.Categories == "Negligible") & (DA['FaultDuration'] == faultDuration)].count())
    # Numbers of Benign
    duration_benign.append(faultDuration)
    numbers_benign.append(DA.FaultDuration[(DA.Categories == "Benign") & (DA['FaultDuration'] == faultDuration)].count())
    # Numbers of Severe
    duration_severe.append(faultDuration)
    numbers_severe.append(DA.FaultDuration[(DA.Categories == "Severe") & (DA['FaultDuration'] == faultDuration)].count())

plt.plot(duration_negligible, numbers_negligible, '+b', linewidth=1, linestyle='dashed')
plt.plot(duration_benign, numbers_benign, '*', color='darkorange', linewidth=1, linestyle='-')
# plt.plot(duration_nonEffective, numbers_nonEffective, '*g', linewidth=1, linestyle='dashed')
plt.plot(duration_severe, numbers_severe, '^r', linewidth=1, linestyle='--')
plt.xlabel('Fault duration (s)', fontsize='22')
plt.ylabel('Number of experiments', fontsize='22')
x_ticks = np.arange(1, 10.1, 1)
plt.xticks(x_ticks)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.gcf().autofmt_xdate()
plt.legend(['Negligible', 'Benign', 'Severe'],  ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={"size":16})
plt.show()
#==================================================================================#
#               Plot: Injection Time vs Number of Experiments                      #
#==================================================================================#
time_negligible = []
time_benign = []
time_severe = []
numbers_negligible = []
numbers_benign = []
numbers_severe = []
# Change the FaultActivationTimeRange according to the selected traffic scenario used
for faultActivationTime in numpy.arange(20, 30.1, 0.5):
    faultActivationTime = round(faultActivationTime, 2)
    # Numbers of Negligible
    time_negligible.append(faultActivationTime)
    numbers_negligible.append(DA.Start_time[(DA.Categories == "Negligible") & (DA['Start_time'] == faultActivationTime)].count())
    # Numbers of Benign
    time_benign.append(faultActivationTime)
    numbers_benign.append(DA.Start_time[(DA.Categories == "Benign") & (DA['Start_time'] == faultActivationTime)].count())
    # Numbers of Severe
    time_severe.append(faultActivationTime)
    numbers_severe.append(DA.Start_time[(DA.Categories == "Severe") & (DA['Start_time'] == faultActivationTime)].count())

fig, ax = plt.subplots()
fig.set_size_inches(12.7, 8.27)
plt.plot(time_negligible, numbers_negligible, '+b', linewidth=1, linestyle='dashed')
plt.plot(time_benign, numbers_benign, '*', color='darkorange', linewidth=1, linestyle='-')
plt.plot(time_severe, numbers_severe, '^r', linewidth=1, linestyle='--')
plt.xlabel('Fault activation time (s)', fontsize='23')
plt.ylabel('Number of experiments', fontsize='23')
x_ticks = np.arange(20.0, 30.1, 0.5)
plt.xticks(x_ticks)
y_ticks = np.arange(0, 251, 25)
plt.yticks(y_ticks)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gcf().autofmt_xdate()
plt.legend(['Negligible', 'Benign', 'Severe'],  ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={"size":17})
plt.show()
#==================================================================================#
#               Plot: Injected Value vs Number of Experiments                      #
#==================================================================================#
Injected_value_negligible = []
Injected_value_benign = []
Injected_value_severe = []
EXnumbers_negligible = []
EXnumbers_benign = []
EXnumbers_severe = []
# Change the FaultValueRange according to the selected fault model such as "Brightness" , "Salt&Pepper"
for faultValue in numpy.arange(0, 7.51, 0.3):
    faultValue = round(faultValue, 2)
    # Numbers of Negligible
    Injected_value_negligible.append(faultValue)
    EXnumbers_negligible.append(DA.Start_time[(DA.Categories == "Negligible") & (DA['Injected_value'] == faultValue)].count())
    # Numbers of Benign
    Injected_value_benign.append(faultValue)
    EXnumbers_benign.append(DA.Start_time[(DA.Categories == "Benign") & (DA['Injected_value'] == faultValue)].count())
    # Numbers of Severe
    Injected_value_severe.append(faultValue)
    EXnumbers_severe.append(DA.Start_time[(DA.Categories == "Severe") & (DA['Injected_value'] == faultValue)].count())

fig, ax = plt.subplots()
fig.set_size_inches(12.7, 8.27)  # size of A4 paper
plt.plot(Injected_value_negligible, EXnumbers_negligible, '+b', linewidth=1, linestyle='dashed')
plt.plot(Injected_value_benign, EXnumbers_benign, '*', color='darkorange', linewidth=1, linestyle='-')
plt.plot(Injected_value_severe, EXnumbers_severe, '^r', linewidth=1, linestyle='--')
# Change the label according to the selected Fault model such as 'Brightness coefficient' or Salt&Pepper noise (%)
plt.xlabel('Brightness coefficient', fontsize='23')
plt.ylabel('Number of experiments', fontsize='23')
# Change the FaultValueRange according to the selected fault model such as "Brightness" , "Salt&Pepper" values
x_ticks = np.arange(0, 7.51, 0.3)
plt.xticks(x_ticks)
y_ticks = np.arange(0, 251, 25)
plt.yticks(y_ticks)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gcf().autofmt_xdate()
plt.legend(['Negligible', 'Benign', 'Severe'],  ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={"size":17})
plt.show()


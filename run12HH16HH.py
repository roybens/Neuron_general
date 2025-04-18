from NeuronModelClass import NeuronModel
from NrnHelper import *
import NrnHelper as nh
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import numpy as np
from Na12HMMModel_TF import *
import Na12HMMModel_TF as tf
import os
import efel_feature_extractor as ef
# from currentscape.currentscape import plot_currentscape
import logging
import pandas as pd
# import Document as doc
# import Tim_ng_functions as nf

sim_config_soma = {
                'section' : 'soma',
                'segment' : 0.5,
                'section_num': 0,
                'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'],
                'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
                'ionic_concentrations' :["cai", "ki", "nai"]
                }

#################################################################################
#1
# sim_config_soma = {
                # 'section' : 'soma',
                # 'segment' : 0.5,
                # 'section_num': 0,
                # #'currents' : ['ina','ica','ik'],
                # 'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
                # #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
                # #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                # #'currents'  : ['ihcn_Ih','ik_SKv3_1','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                # 'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
                # 'ionic_concentrations' :["cai", "ki", "nai"]
                # #'ionic_concentrations' :["ki", "nai"]
                # }
# 2
sim_config_ais = {
                'section' : 'axon',
                'segment' : 0.1,
                'section_num': 0,
                #'currents' : ['ina','ica','ik'],
                #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
                'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
                #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                #'currents'  : ['ihcn_Ih','ik_SKv3_1','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
                #'ionic_concentrations' :["cai", "ki", "nai"]
                'ionic_concentrations' :["ki", "nai"]
                }
# 3
sim_config_basaldend = {
                'section' : 'dend',
                'segment' : 0.5,
                'section_num': 70,
                #'currents' : ['ina','ica','ik'],
                #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
                #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
                #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                'currents'  : [], #dend (no Ih, no ik_SKv3_1)
                'current_names' : ['Ih','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
                #'ionic_concentrations' :["cai", "ki", "nai"]
                'ionic_concentrations' :[]
                }
#4
sim_config_nexus = {
                'section' : 'apic',
                'segment' : 0,
                'section_num': 77,
                #'currents' : ['ina','ica','ik'],
                #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
                'currents'  : ['ik_SKv3_1'], #Nexus
                #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                
                'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
                #'ionic_concentrations' :["cai", "ki", "nai"]
                'ionic_concentrations' :["ki", "nai"]
                }
#5
sim_config_apicaldend = {
                'section' : 'apic',
                'segment' : 0.5,
                'section_num': 90,
                # 'currents' : ['ina','ica','ik'],
                #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
                'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ik_SKv3_1','ihcn_Ih'], #AIS (no Ih)
                #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                #'currents'  : ['ihcn_Ih','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                # 'ionic_concentrations' :["cai", "ki", "nai"]
                'ionic_concentrations' :["ki", "nai"]
                }
#################################################################################

def modify_dict_file(filename, changes):
  """
  Modifies values in a dictionary stored in a text file.

  Args:
      filename: The name of the text file containing the dictionary.
      changes: A dictionary containing key-value pairs where the key is the key to modify in the original dictionary and the value is the new value.

  Raises:
      ValueError: If the file cannot be opened or the content is not valid JSON.
  """

  try:
    # Open the file and read its content
    with open(filename, "r") as file:
      content = file.read()

    # Try to load the content as a dictionary
    try:
      data = eval(content)  # Assuming the file contains valid dictionary syntax
    except (NameError, SyntaxError):
      raise ValueError("Invalid dictionary format in the file.")

    # Modify values based on the provided changes dictionary
    for key, value in changes.items():
      if key not in data:
        print(f"Warning: Key '{key}' not found in the dictionary, skipping.")
      else:
        data[key] = value

    # Write the modified dictionary back to the file
    # with open(filename, "w") as file:
    #   file.write(repr(data))
    with open(filename, "w") as file:
      file.write(json.dumps(data, indent=2))  # Add indentation for readability (optional)

  except IOError as e:
    raise ValueError(f"Error opening or writing file: {e}")
  

  #Don't forget to change NeuronModelClass.py to './Neuron_Model_12HH16HH/' and recompile!!


root_path_out = './Plots/12HH16HH/' ##path for saving your plots
if not os.path.exists(root_path_out): ##make directory if it doens't exist
        os.makedirs(root_path_out)


## Text files with HH params that will be modified later
filename12 = './params/na12annaTFHH2.txt' ##12HH params file that you will update with values below in changesna12
filename16 = './params/na16HH_TF2.txt' ##16HH params file that you will update with values below in changesna16
filenamemut = './params/na12annaTFHHmut.txt' 



## 1.2HH params newest after Kevin's inpurt. 12-16 gap closer to 5mV now.
changesna12={"Rd": 0.023204006298533603, "Rg": 0.015604498120126004, "Rb": 0.0925081211054913, "Ra": 0.23933332265451177, "a0s": 0.0005226303768198727, "gms": 0.14418575154491814, "hmin": 0.008449935591049326, "mmin": 0.01193016441163175, "qinf": 5.7593653647578105, "q10": 2.1532859986639186, "qg": 1.2968193480468215, "qd": 0.661199851452832, "qa1": 4.492758160759386, "smax": 3.5557932199839737, "sh": 8.358558450280716, "thinf": -47.8194205612529, "thi2": -79.6556083820085, "thi1": -62.40165437813537, "tha": -33.850064879126805, "vvs": 1.4255479951467982, "vvh": -55.33213046147061, "vhalfs": -40.89976480829731, "zetas": 13.403615755952343}

## 16HH mod file params can be changed below
changesna16 = {"Rd": 0.03, "Rg": 0.01, "Rb": 0.124, "Ra": 0.4, "a0s": 0.0003, "gms": 0.2, "hmin": 0.01, "mmin": 0.02, "qinf": 7, "q10": 2, "qg": 1.5, "qd": 0.5, "qa1": 7.2, "smax": 10, "sh": 8, "thinf": -51.5, "thi2": -47.5, "thi1": -47.5, "tha": -33.5, "vvs": 2, "vvh": -58, "vhalfs": -26.5, "zetas": 12}

modify_dict_file(filename12, changesna12)
modify_dict_file(filename16, changesna16)


config_dict = {"sim_config_soma": sim_config_soma,
              "sim_config_ais": sim_config_ais,
              "sim_config_basaldend": sim_config_basaldend,
              "sim_config_nexus": sim_config_nexus,
              "sim_config_apicaldend": sim_config_apicaldend}

config_dict2={"sim_config_nexus": sim_config_nexus,
              "sim_config_apicaldend": sim_config_apicaldend}

config_dict3={"sim_config_soma": sim_config_soma}

for config_name, config in config_dict3.items():
  path = f'14-TestPlot_forBen'

 


## Use this line to instantiate a pandas dataframe to store all the features
# allmutsefel = pd.DataFrame()


simwt = tf.Na12Model_TF(ais_nav12_fac=5.76,ais_nav16_fac=1.08,
                              nav12=1.1,nav16=1.43, somaK=0.022, KP=3.9375, KT=5,
                              ais_ca = 43,ais_Kca = 0.25,
                              soma_na16=0.8,soma_na12=2.56,node_na = 1,
                              dend_nav12=1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
wt_Vm1,_,wt_t1,_ = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=400, sim_config = config) #stim_amp=0.5
# wt_fi=simwt.plot_fi_curve_2line(wt_data=None,wt2_data=None,start=-0.4,end=1,nruns=140, fn=f'WT_FI', epochlabel='200ms')
# features_wt = ef.get_features(sim=simwt, prefix=f'{root_path_out}/{path}/WT', mut_name='WT')
# allmutsefel = allmutsefel.append(features_wt, ignore_index=True)

## This line will plot the channel densities in the axon[0] section of the model
# NeuronModel.chandensities(name = f'{root_path_out}/densities_WT') ##TF uncomment to run function and plot channel densities in axon[0]


## These 4 lines of code will plot the voltage and dV/dt of the soma for a single simulation
# fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
# simwt.plot_stim(axs = axs[0],stim_amp = 0.3,dt=0.005, clr='cadetblue')
# plot_dvdt_from_volts(simwt.volt_soma, simwt.dt, axs[1],clr='cadetblue')
# fig_volts.savefig(f'{simwt.plot_folder}/WT_test.pdf') #Change output file path here

## Variable with multiple mutants and their corresponding parameters
migraine={"F257I":{"Rd": 0.028485318424710374, "Rg": 0.018420814026814298, "Rb": 0.05777962337521357, "Ra": 0.21341303335597034, "a0s": 0.00046381351100748496, "gms": 0.1341164855099387, "hmin": 0.006864146828635849, "mmin": 0.007621368015226187, "qinf": 6.486459886532015, "q10": 2.561051746368186, "qg": 1.3943995618682714, "qd": 0.797072687262635, "qa1": 6.540179485338942, "smax": 5.751234160342341, "sh": 9.898965372911075, "thinf": -42.299802571430824, "thi2": -64.0747495998566, "thi1": -48.0852551990378, "tha": -30.139992632180743, "vvs": 0.8468560048684934, "vvh": -53.739541326283735, "vhalfs": -42.22939001512733, "zetas": 12.811495608869796},
"R1319G":{"Rd": 0.01821017957894782, "Rg": 0.015835927879902578, "Rb": 0.08669778691261865, "Ra": 0.25222138069588795, "a0s": 0.0005998602174497901, "gms": 0.15734865667490094, "hmin": 0.003049022325449447, "mmin": 0.009227432163769297, "qinf": 7.542037850663156, "q10": 1.3991326492121134, "qg": 0.11658354700541385, "qd": 0.41022807889968216, "qa1": 6.23800810747929, "smax": 2.297618044174789, "sh": 9.225725362157418, "thinf": -46.09023665760313, "thi2": -57.0320710747067, "thi1": -62.70708396987019, "tha": -29.27378295119758, "vvs": 0.25717057711770985, "vvh": -58.74304862555019, "vhalfs": -31.258170795759927, "zetas": 10.786789360357215},
"K1480E":{"Rd": 0.017988222179818, "Rg": 0.014526835880098123, "Rb": 0.032287886870504066, "Ra": 0.20374071568963156, "a0s": 0.00043332968046547453, "gms": 0.2506541588105391, "hmin": 0.003724133667885614, "mmin": 0.022703936878165614, "qinf": 8.056557948665372, "q10": 2.1947359595099254, "qg": 1.607903072936985, "qd": 0.9369754615041643, "qa1": 6.825173338201797, "smax": 9.756858258324922, "sh": 9.29652730203526, "thinf": -44.454878232047506, "thi2": -78.8896576923306, "thi1": -61.97876376872753, "tha": -25.286365983599477, "vvs": 0.665802756552117, "vvh": -45.45240491205891, "vhalfs": -18.50057219270583, "zetas": 11.579233310014331},
"E999K":{"Rd": 0.026143636968066552, "Rg": 0.01668223028930355, "Rb": 0.014291884348195151, "Ra": 0.3173306743768715, "a0s": 0.0005030781620195419, "gms": 0.2257551972957173, "hmin": 0.01486999595016371, "mmin": 0.01069596553673631, "qinf": 4.543449675893968, "q10": 2.905858138508142, "qg": 1.070567987818106, "qd": 0.8859991427475545, "qa1": 2.7332610992423385, "smax": 4.562540093135402, "sh": 8.697260358969865, "thinf": -40.098974160495985, "thi2": -79.86939611595125, "thi1": -59.571867025996255, "tha": -25.969320595959655, "vvs": 0.05603301531867544, "vvh": -47.92236852687354, "vhalfs": -24.29418118596604, "zetas": 11.472449828098517},}

timfactor=20
e9altered={"E999K":{"Rd": 0.026143636968066552, "Rg": 0.01668223028930355, "Rb": 0.014291884348195151, "Ra": 0.3173306743768715, "a0s": 0.0005030781620195419, "gms": 0.2257551972957173, "hmin": 0.01486999595016371, "mmin": 0.01069596553673631, "qinf": 4.543449675893968, "q10": 2.905858138508142, "qg": 1.070567987818106, "qd": 0.8859991427475545, "qa1": 2.7332610992423385, "smax": 4.562540093135402, "sh": 8.697260358969865, "thinf": -40.098974160495985+timfactor, "thi2": -79.86939611595125+timfactor, "thi1": -59.571867025996255+timfactor, "tha": -25.969320595959655+timfactor, "vvs": 0.05603301531867544, "vvh": -47.92236852687354, "vhalfs": -24.29418118596604+timfactor, "zetas": 11.472449828098517}}


for mutname,dict in e9altered.items():
  print(f"mutname is {mutname}")
  print(f"it's corresponding dictionary is {dict}")
  modify_dict_file(filenamemut,dict)
#   # modify_dict_file(filename16,dict)


##Mutant/Variant
  simmut = tf.Na12Model_TF(ais_nav12_fac=5.76,ais_nav16_fac=1.08,
                              nav12=1.1,nav16=1.43, somaK=0.022, KP=3.9375, KT=5,
                              ais_ca = 43,ais_Kca = 0.25,
                              soma_na16=0.8,soma_na12=2.56,node_na = 1,
                              dend_nav12=1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHHmut',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  
  simmut.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5],stim_dur=400, fnpre=f'{mutname}-t5+20')


  ## Get e-features and append to csv
  #   features_df1 = ef.get_features(sim=simmut, prefix=f'{root_path_out}/{path}', mut_name = f'{mutname}')
  #   allmutsefel = allmutsefel.append(features_df1,ignore_index=True)
  # allmutsefel.to_csv(f'{root_path_out}/{path}/allsynthmuts_EFEL_111524b.csv')
    

  ## Currentscape plotting
  # simmut.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200,pfx=f'{mutname}-')
  

  ## Plot FI curve of WT vs mutant
  # simmut.plot_fi_curve_2line(wt_data=wt_fi,wt2_data=None,start=-0.4,end=1,nruns=140, fn=f'{mutname}-FI', epochlabel='200ms')


  ## Getting raw data for currents
  # mut_Vm1,mut_I1,mut_t1,_ = simmut.get_stim_raw_data(stim_amp = 0.5,dt=0.01,rec_extra=False,stim_dur=500, sim_config = config) #stim_amp=0.5
  
  # ##### Writing all raw data to csv
  # with open(f"{root_path_out}/{mutname}_rawdata.csv",'w',newline ='') as csvfile:
  #   writer = csv.writer(csvfile, delimiter = ',')
  #   #writer.writerow(current_names)
  #   writer.writerow(mut_I1.keys())
    
  #   writer.writerows(mut_I1[x] for x in mut_I1) # This and line below for writing data from entire sweep_len
  #   writer.writerow(mut_Vm1)

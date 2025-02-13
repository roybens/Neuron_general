from NeuronModelClass import NeuronModel
from NrnHelper import *
import NrnHelper as nh
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
from pathlib import Path
import numpy as np
from Na12HMMModel_TF import *
import Na12HMMModel_TF as tf
import os
import efel_feature_extractor as ef
from currentscape.currentscape import plot_currentscape
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


root_path_out = './Plots/12HH16HH/10-KevinRtR_chandensities' ##path for saving your plots
if not os.path.exists(root_path_out): ##make directory if it doens't exist
        os.makedirs(root_path_out)




filename12 = './params/na12annaTFHH2.txt' ##12HH params file that you will update with values below in changesna12
filename16 = './params/na16HH_TF2.txt' ##16HH params file that you will update with values below in changesna16
filenamemut = './params/na12annaTFHHmut.txt' 



rbs_vshift = 13.5
## 1.2HH params newest after Kevin's inpurt. 12-16 gap closer to 5mV now.
changesna12={"Rd": 0.023204006298533603, "Rg": 0.015604498120126004, "Rb": 0.0925081211054913, "Ra": 0.23933332265451177, "a0s": 0.0005226303768198727, "gms": 0.14418575154491814, "hmin": 0.008449935591049326, "mmin": 0.01193016441163175, "qinf": 5.7593653647578105, "q10": 2.1532859986639186, "qg": 1.2968193480468215, "qd": 0.661199851452832, "qa1": 4.492758160759386, "smax": 3.5557932199839737, "sh": 8.358558450280716, "thinf": -47.8194205612529, "thi2": -79.6556083820085, "thi1": -62.40165437813537, "tha": -33.850064879126805, "vvs": 1.4255479951467982, "vvh": -55.33213046147061, "vhalfs": -40.89976480829731, "zetas": 13.403615755952343}
## 16HH mod file params can be changed below
changesna16 = {"Rd": 0.03, "Rg": 0.01, "Rb": 0.124, "Ra": 0.4, "a0s": 0.0003, "gms": 0.2, "hmin": 0.01, "mmin": 0.02, "qinf": 7, "q10": 2, "qg": 1.5, "qd": 0.5, "qa": 7.2, "smax": 10, "sh": 8, "thinf": -51.5, "thi2": -47.5, "thi1": -47.5, "tha": -33.5, "vvs": 2, "vvh": -58, "vhalfs": -26.5, "zetas": 12}
# changesna16 = {"sh": 8, "tha": -47+rbs_vshift, "qa": 7.2, "Ra": 0.4, "Rb": 0.124, "thi1": -61+rbs_vshift, "thi2": -61+rbs_vshift, "qd": 0.5, "qg": 1.5, "mmin": 0.02, "hmin": 0.01, "q10": 2, "Rg": 0.01, "Rd": 0.03, "thinf": -65+rbs_vshift, "qinf": 7, "vhalfs": -40+rbs_vshift, "a0s": 0.0003, "gms": 0.2, "zetas": 12, "smax": 10, "vvh": -58, "vvs": 2, "ar2": 1}

modify_dict_file(filename12, changesna12)
modify_dict_file(filename16, changesna16)


# config_dict = {"sim_config_soma": sim_config_soma,
#               "sim_config_ais": sim_config_ais,
#               "sim_config_basaldend": sim_config_basaldend,
#               "sim_config_nexus": sim_config_nexus,
#               "sim_config_apicaldend": sim_config_apicaldend}

# config_dict2={"sim_config_nexus": sim_config_nexus,
#               "sim_config_apicaldend": sim_config_apicaldend}

config_dict3={"sim_config_soma": sim_config_soma}

for config_name, config in config_dict3.items():
  path = f'1-WT_baseline'

allmutsefel = pd.DataFrame()
# fig,axs = plt.subplots(1,1)
fig1, axs1 = plt.subplots(figsize=(cm_to_in(8), cm_to_in(8)))
fig2, axs2 = plt.subplots(figsize=(cm_to_in(8), cm_to_in(8)))
fig3, axs3 = plt.subplots(figsize=(cm_to_in(8), cm_to_in(8)))
cmap = cm.get_cmap('rainbow')

ratios1216 = {
  'test':(1,1),
  '100:0': (1, 0),
  '90:10': (0.9, 0.1),
  '80:20': (0.8, 0.2),
  '70:30': (0.7, 0.3),
  '60:40': (0.6, 0.4),
  '50:50': (0.5, 0.5),
  '40:60': (0.4, 0.6),
  '30:70': (0.3, 0.7),
  '20:80': (0.2, 0.8),
  '10:90': (0.1, 0.9),
  '0:100': (0, 1)
}
chantest ={'test':(2,1)}

for key, (fac12, fac16) in chantest.items():
  # 56color = cmap(i/11)
  # tempfac=2
  simwt = tf.Na12Model_TF(ais_nav12_fac=12*1.2*fac12,ais_nav16_fac=12*0.6*fac16,nav12=1*fac12,nav16=1.3*fac16, somaK=1*2.2*0.01, KP=25*0.15, KT=5,#ais_nav12_fac=12*fac*factor,ais_nav16_fac=12*0.75
                                    ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1*0.8,soma_na12=3.2*0.8,node_na = 1,
                                    na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                    na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                    plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  # wt_Vm1,_,wt_t1,_ = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=1700, sim_config = config) #stim_amp=0.5
  # wt_fi=simwt.plot_fi_curve_2line(wt_data=None,wt2_data=None,start=-0.4,end=1,nruns=140, fn=f'WT_FI', epochlabel='200ms')
  # # simwt.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200,pfx=f'WT-')
  # simwt.make_currentscape_plot(amp=0.5, time1=50,time2=300,stim_start=30, sweep_len=500,pfx=f'WT-')
#   features_wt = ef.get_features(sim=simwt, prefix=f'{root_path_out}/{path}/WT', mut_name='WT')
# allmutsefel = allmutsefel.append(features_wt, ignore_index=True)

  # NeuronModel.chandensities(name = f'{root_path_out}/{path}/densities_WT') ## doesn't include soma/dendrite
  NeuronModel.chandensities2(name = f'{root_path_out}/{path}/WT_gauAIS_12-{fac12}_16-{fac16}_121segments_test4') ## includes soma/dendrites

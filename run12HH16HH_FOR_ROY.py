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


root_path_out = './Plots/12HH16HH/5-newAIS_raiseDVDT' ##path for saving your plots
if not os.path.exists(root_path_out): ##make directory if it doens't exist
        os.makedirs(root_path_out)


rbs_vshift = 13.5

filename12 = './params/na12annaTFHH2.txt' ##12HH params file that you will update with values below in changesna12
filename16 = './params/na16HH_TF2.txt' ##16HH params file that you will update with values below in changesna16

## 12HH mod file params can be changed below
# changesna12 = {
#         "sh": 8,
#         "tha": -38+rbs_vshift,
#         "qa": 5.41,
#         "Ra": 0.3282,
#         "Rb": 0.1,
#         "thi1": -80+rbs_vshift,#-80,
#         "thi2": -80+rbs_vshift,#-80,
#         "qd": 0.5,
#         "qg": 1.5,
#         "mmin": 0.02,
#         "hmin": 0.01,
#         "Rg": 0.01,
#         "Rd": 0.02657,
#         "thinf": -53+rbs_vshift,
#         "qinf": 7.69,
#         "vhalfs": -60+rbs_vshift,
#         "a0s": 0.0003,
#         "gms": 0.2,
#         "q10": 2,
#         "zetas": 12,
#         "smax": 10,
#         "vvh": -58,
#         "vvs": 2,
#         "ar2": 1,
#         "Ena": 55,
#         }

## 1.2 HH params after re-fitting rbs_vshift 1.2. The rbs_vshift had weird inactivation curve that didn't bottom out at 0.
changesna12={"Rd": 0.025712394696815438, "Rg": 0.01854277725353276, "Rb": 0.09013136340161398, "Ra": 0.3380714915775742, "a0s": 0.00036615946706607756, "gms": 0.14082624570054866, "hmin": 0.008420778920829085, "mmin": 0.013671131800210966, "qinf": 5.760329120353593, "q10": 2.289601426305275, "qg": 0.6693522946835427, "qd": 0.8058343822410788, "qa1": 5.835550042292994, "smax": 5.941545585888373, "sh": 8.886047186457889, "thinf": -40.114984963535186, "thi2": -77.41692349310195, "thi1": -60.488477521934875, "tha": -24.155451306086988, "vvs": 0.7672523706054653, "vvh": -53.184249317587984, "vhalfs": -33.73363659219147, "zetas": 13.419130866269455}

## 16HH mod file params can be changed below
changesna16 = {
        "sh": 8,
        "tha": -47+rbs_vshift,
        "qa": 7.2,
        "Ra": 0.4,
        "Rb": 0.124,
        "thi1": -61+rbs_vshift,
        "thi2": -61+rbs_vshift,
        "qd": 0.5,
        "qg": 1.5,
        "mmin": 0.02,  
        "hmin": 0.01,  
        "q10": 2,
        "Rg": 0.01,
        "Rd": 0.03,
        "thinf": -65+rbs_vshift,
        "qinf": 7,
        "vhalfs": -40+rbs_vshift,
        "a0s": 0.0003,
        "gms": 0.2,
        "zetas": 12,
        "smax": 10,
        "vvh": -58,
        "vvs": 2,
        "ar2": 1,
        #"ena": 55
        }

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
# path = f'1-m1879t'
# config = sim_config_soma
# wt_fi = [0, 0, 0, 0, 1, 7, 9, 10, 11, 12, 13, 14, 14, 15, 16, 16, 17, 17, 18, 18, 19]
# het_fi = [0, 0, 0, 0, 1, 7, 9, 10, 11, 12, 13, 14, 15, 16, 16, 17, 17, 18, 19, 19, 20]

# wt_fi = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,3,3,4,4,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,9,9,10,10,10,10,10,10,11,11,11,11,11,11,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,14,14,14,14,14,14,14,14,14,15,15,15,15,15,15,15,15,15,16,16,16,16,16,16,16]
# het_fi = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,3,4,4,4,5,5,6,6,6,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,11,11,11,11,12,12,12,12,12,12,13,13,13,13,13,13,14,14,14,14,14,14,15,15,15,15,15,15,15,16,16,16,16,16,16,16,16,17,17,17,17,17,17,17,17,18,18,18,18,18,18,18]
# ko_fi = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,3,3,4,4,5,5,6,6,6,7,7,7,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,13,13,13,13,13,14,14,14,14,14,14,15,15,15,15,15,15,16,16,16,16,16,16,17,17,17,17,17,17,17,18,18,18,18,18,18,18,19,19,19,19,19,19,19,19,20,20]

for config_name, config in config_dict3.items():
  path = f'41-scans_newAIS_morecelllike'
# simwt = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1*2.2, KP=25*0.15, KT=5,
#                               ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1,soma_na12=3.2,node_na = 1,
#                               na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
#                               na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
#                               plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
# wt_Vm1,_,wt_t1,_ = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)

  # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = config) #sim_config for changing regions
  # simwt.plot_fi_curve_2line(wt_data=None,wt2_data=None,start=0,end=2,nruns=21, fn=f'{path}/WT_FIcurve.pdf')
  # simwt.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WT')
# simwt.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200, pfx='WT')
# simwt.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WT')

# NeuronModel.chandensities(name = f'{root_path_out}/densities_WT') ##TF uncomment to run function and plot channel densities in axon[0]

# fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
# simwt.plot_stim(axs = axs[0],stim_amp = 0.3,dt=0.005, clr='cadetblue')
# plot_dvdt_from_volts(simwt.volt_soma, simwt.dt, axs[1],clr='cadetblue')
# fig_volts.savefig(f'{simwt.plot_folder}/WT_300pA.pdf') #Change output file path here 

# m1879t = {'Rd': 0.013285, 'Rg': 0.01, 'Rb': 0.1, 'Ra': 0.3282, 'a0s': 0.0003, 'gms': 0.2, 'hmin': 0.01, 'mmin': 0.02, 'qinf': 7.69, 'q10': 2, 'qg': 1.5, 'qd': 0.5, 'qa': 5.41, 'smax': 10, 'sh': 8, 'thinf': -30.2, 'thi2': -57.2, 'thi1': -57.2, 'tha': -22, 'vvs': 2, 'vvh': -58, 'vhalfs': -37.2, 'zetas': 12}
# e1211k = {'Rd': 0.02657, 'Rg': 0.01, 'Rb': 0.1, 'Ra': 0.3282, 'a0s': 0.0003, 'gms': 0.2, 'hmin': 0.01, 'mmin': 0.02, 'qinf': 7.69, 'q10': 2, 'qg': 1.5, 'qd': 0.5, 'qa': 5.41, 'smax': 10, 'sh': 8, 'thinf': -56.15, 'thi2': -83.15, 'thi1': -83.15, 'tha': -33.6, 'vvs': 2, 'vvh': -58, 'vhalfs': -63.15, 'zetas': 12}
# modify_dict_file(filename12,newwt)


# E1211K_fit = {"Rd": 0.02997147068228529, "Rg": 0.008897343211993404, "Rb": 0.1905632165201543, "Ra": 0.17021304035954068, "a0s": 0.0004623172353304141, "gms": 0.06823404793686191, "hmin": 0.006840457920016884, "mmin": 0.011385473619953321, "qinf": 9.955469461805416, "q10": 2.26803894306103, "qg": 2.891931568518361, "qd": 0.6831763145330393, "qa1": 3.9430916086277943, "smax": 2.291423740934766, "sh": 9.368077641872159, "thinf": -51.52172304144173, "thi2": -60.433480791446335, "thi1": -67.17190725995887, "tha": -34.52344084985742, "vvs": 2.35878838817752, "vvh": -60.859242318800554, "vhalfs": -37.1233573147436, "zetas": 14.835757964655997}
# M1879T_fit = {"Rd": 0.01869558161227628, "Rg": 0.014742011298945906, "Rb": 0.09039075777185525, "Ra": 0.35963455171363023, "a0s": 0.00014227805632812505, "gms": 0.255082958443083, "hmin": 0.001926533350955973, "mmin": 0.02456425796235449, "qinf": 7.293897980026858, "q10": 1.9340817795282903, "qg": 2.710511377603585, "qd": 0.17490503650016742, "qa1": 6.418759772577477, "smax": 10.235848311910516, "sh": 9.018629437597378, "thinf": -26.434602737525683, "thi2": -56.49953744144141, "thi1": -44.65364934653208, "tha": -16.411116454184114, "vvs": 2.1182888485979667, "vvh": -53.778899069537054, "vhalfs": -46.45143392507821, "zetas": 8.610440928204904}
# r850p = {"Rd": 0.026028590561607057, "Rg": 0.01462201143223921, "Rb": 0.06940454866111936, "Ra": 0.3994888778516782, "a0s": 0.0004633732029466548, "gms": 0.2466005657502548, "hmin": 0.011092316147529334, "mmin": 0.02856133390485918, "qinf": 8.243477619364711, "q10": 1.5391582444238114, "qg": 1.8772774806842443, "qd": 0.21192765348993275, "qa1": 6.7338622255775835, "smax": 13.672179701011997, "sh": 5.592957065021524, "thinf": -43.06853111008826, "thi2": -77.98323725555565, "thi1": -66.71276444361911, "tha": -11.750602743874275, "vvs": 1.2137870369006865, "vvh": -47.96500165314955, "vhalfs": -37.93117875585497, "zetas": 4.993862532257029}
# modify_dict_file(filename12,r850p)

# for mutname,dict in muts.items():
#   print(f"mutname is {mutname}")
#   print(f"it's corresponding dictionary is {dict}")
#   modify_dict_file(filename12,dict)
#   # modify_dict_file(filename16,dict)


# for factor in [0.00001,0.0001,0.001,0.01,0.1,0.25,0.5,0.75,1,1.2,2,4,6,10,25,50,100,1000,10000,100000]:
# for amps in np.arange(-0.4,0.4,0.05):
for factor in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]:

# ##Mutant/Variant
# simmut = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1*2.2, KP=25*0.15, KT=5,
#                             ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1,soma_na12=3.2,node_na = 1,
#                             na12name = 'na12annaTFHH',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
#                             na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
#                             plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
# simmut.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'newWt')

  ## WT vs HET vs Mut  
  ##WT model
  simwt = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12*factor,nav12=1,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1*0.8,soma_na12=3.2*0.8,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  wt_Vm1,_,wt_t1,_ = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = config) #stim_amp=0.5
  # wt_fi=simwt.plot_fi_curve_2line(wt_data=None,wt2_data=None,start=-0.4,end=1,nruns=140, fn=f'WT')
  # simwt.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200,pfx='WT')
  # NeuronModel.chandensities(name = f'{root_path_out}/{path}/densities_WT') ##TF uncomment to run function and plot channel densities in axon[0]
  
  # features_df1 = ef.get_features(sim=simwt, prefix='WT', mut_name = 'na12annaTFHH2')
  


  # ##het model
  sim_het = tf.Na12Model_TF(ais_nav12_fac=6,ais_nav16_fac=12*factor,nav12=0.5,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=0.8+0.2*0.8,soma_na12=3.6-0.4*0.8,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  het_Vm1,_,het_t1,_ = sim_het.get_stim_raw_data(stim_amp =0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = config) #sim_config for changing regions
  # het_fi=sim_het.plot_fi_curve_2line(wt_data=wt_fi,wt2_data=None,start=-0.4,end=1,nruns=140, fn=f'WTHET')
  # sim_het.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=config,vs_amp=[0.5], fnpre=f'WTvsHET')#sim_config for changing regions
  # sim_het.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200,pfx='HET')
  # NeuronModel.chandensities(name = f'{root_path_out}/{path}/densities_Het') ##TF uncomment to run function and plot channel densities in axon[0]
  # features_df2 = ef.get_features(sim=sim_het, prefix='HET', mut_name = 'na12annaTFHH2')
  


  # ##KO model
  sim_ko = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12*factor,nav12=0,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=0,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  # sim_ko.plot_fi_curve_2line(wt_data=wt_fi,wt2_data=het_fi,start=-0.4,end=1,nruns=140, fn=f'WTHETKO')
  sim_ko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,het_Vm=het_Vm1,het_t=het_t1,sim_config=config,vs_amp=[0.5], fnpre=f'WTvHETvKO_ais16-{factor}')#vs_amp=[0.5]
  # sim_ko.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200,pfx='KO')
  # NeuronModel.chandensities(name = f'{root_path_out}/{path}/densities_KO') ##TF uncomment to run function and plot channel densities in axon[0]
  # features_df3 = ef.get_features(sim=sim_ko, prefix='KO', mut_name = 'na12annaTFHH2')

  sim16 = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12*0.1*factor,nav12=1,nav16=1.3*0.1, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                                ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1*0.8,soma_na12=3.2*0.8,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  Vm,_,t,_ = sim16.get_stim_raw_data(stim_amp =0.5 ,dt=0.005,rec_extra=False,stim_dur=500, sim_config = config) #stim_amp=0.5
  
  sim16ko = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12*0,nav12=1,nav16=1.3*0, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                                ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1*0.8,soma_na12=3.2*0.8,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  sim16ko.wtvsmut_stim_dvdt(wt_Vm=Vm,wt_t=t,het_Vm=None,het_t=None,sim_config=config,vs_amp=[0.5], fnpre=f'WTvHETvKO_ais16_16ko-{factor}')#vs_amp=[0.5]

 


  '''
  ##SomaK
  ##WT model
  simwt_somaK = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1*2.2*0.01*factor, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1,soma_na12=3.2,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  wt_Vm1,_,wt_t1,_ = simwt_somaK.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##het model
  sim_het_somaK = tf.Na12Model_TF(ais_nav12_fac=6,ais_nav16_fac=12,nav12=0.5,nav16=1.3, somaK=1*2.2*0.01*factor, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=3.6-0.4,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  het_Vm1,_,het_t1,_ = sim_het_somaK.get_stim_raw_data(stim_amp =0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##KO model
  sim_ko_somaK = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12,nav12=0,nav16=1.3, somaK=1*2.2*0.01*factor, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=0,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  sim_ko_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,het_Vm=het_Vm1,het_t=het_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvHETvKO_somaK-{factor}')
  

  ##KP
  ##WT model
  simwt_KP = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15*factor, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1,soma_na12=3.2,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  wt_Vm1,_,wt_t1,_ = simwt_KP.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##het model
  sim_het_KP = tf.Na12Model_TF(ais_nav12_fac=6,ais_nav16_fac=12,nav12=0.5,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15*factor, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=3.6-0.4,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  het_Vm1,_,het_t1,_ = sim_het_KP.get_stim_raw_data(stim_amp =0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##KO model
  sim_ko_KP = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12,nav12=0,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15*factor, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=0,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  sim_ko_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,het_Vm=het_Vm1,het_t=het_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvHETvKO_KP-{factor}')
  

  ##KT
  ##WT model
  simwt_KT = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5*factor,
                            ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1,soma_na12=3.2,node_na = 1,
                            na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                            na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                            plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  wt_Vm1,_,wt_t1,_ = simwt_KT.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##het model
  sim_het_KT = tf.Na12Model_TF(ais_nav12_fac=6,ais_nav16_fac=12,nav12=0.5,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5*factor,
                            ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=3.6-0.4,node_na = 1,
                            na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                            na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                            plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  het_Vm1,_,het_t1,_ = sim_het_KT.get_stim_raw_data(stim_amp =0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##KO model
  sim_ko_KT = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12,nav12=0,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5*factor,
                            ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=0,node_na = 1,
                            na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                            na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                            plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  sim_ko_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,het_Vm=het_Vm1,het_t=het_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvHETvKO_KT-{factor}')


  ##ais_ca
  ##WT model
  simwt_AISCA = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1*factor,ais_Kca = 0.5,soma_na16=1,soma_na12=3.2,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  wt_Vm1,_,wt_t1,_ = simwt_AISCA.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##het model
  sim_het_AISCA = tf.Na12Model_TF(ais_nav12_fac=6,ais_nav16_fac=12,nav12=0.5,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1*factor,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=3.6-0.4,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  het_Vm1,_,het_t1,_ = sim_het_AISCA.get_stim_raw_data(stim_amp =0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##KO model
  sim_ko_AISCA = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12,nav12=0,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1*factor,ais_Kca = 0.5,soma_na16=0.8+0.2,soma_na12=0,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  sim_ko_AISCA.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,het_Vm=het_Vm1,het_t=het_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvHETvKO_AISCA-{factor}')
 
 
  
  ##ais_Kca
  ##WT model
  simwt_aisKca = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5*factor,soma_na16=1,soma_na12=3.2,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  wt_Vm1,_,wt_t1,_ = simwt_aisKca.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##het model
  sim_het_aisKca = tf.Na12Model_TF(ais_nav12_fac=6,ais_nav16_fac=12,nav12=0.5,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5*factor,soma_na16=0.8+0.2,soma_na12=3.6-0.4,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  het_Vm1,_,het_t1,_ = sim_het_aisKca.get_stim_raw_data(stim_amp =0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
  ##KO model
  sim_ko_aisKca = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12,nav12=0,nav16=1.3, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5*factor,soma_na16=0.8+0.2,soma_na12=0,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  sim_ko_aisKca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,het_Vm=het_Vm1,het_t=het_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvHETvKO_aisKca-{factor}')
  '''
















'''
  for fac in [0.15]:
    
    
    sim_ais12 = tf.Na12Model_TF(ais_nav12_fac=12*fac,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                ais_ca = 100,ais_Kca = 0.5,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_ais12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais12-{fac}')
    
    
    sim_ais16 = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12*fac,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                ais_ca = 100,ais_Kca = 0.5,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_ais16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais16-{fac}')
    
    
    sim_n12 = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1*fac,nav16=1.3, somaK=1, KP=25, KT=5,
                                ais_ca = 100,ais_Kca = 0.5,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_n12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'n12-{fac}')
    

    sim_n16 = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3*fac, somaK=1, KP=25, KT=5,
                                ais_ca = 100,ais_Kca = 0.5,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_n16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'n16-{fac}')
    

    sim_somaK = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1*fac, KP=25, KT=5,
                                ais_ca = 100,ais_Kca = 0.5,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK-{fac}')
    

    sim_KP = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25*fac, KT=5,
                                ais_ca = 100,ais_Kca = 0.5,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP-{fac}')
    

    sim_KT = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5*fac,
                                ais_ca = 100,ais_Kca = 0.5,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT-{fac}')
    

    sim_aisca = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                ais_ca = 100*fac,ais_Kca = 0.5,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_aisca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'aisca-{fac}')
    

    sim_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                ais_ca = 100,ais_Kca = 0.5*fac,soma_na16=1,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca-{fac}')
    

    sim_soma_na16 = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                ais_ca = 100,ais_Kca = 0.5,soma_na16=1*fac,soma_na12 =3.2,node_na = 1,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/', update=True)
    sim_soma_na16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na16-{fac}')
  '''
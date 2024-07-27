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


root_path_out = './Plots/12HH16HH_RBS/HH_mutants_072724' ##path for saving your plots
if not os.path.exists(root_path_out): ##make directory if it doens't exist
        os.makedirs(root_path_out)


##Enter values that you want to change in the neuron model (specific vals array or evenly spaced numpy array)
vals =[1]
vals2 = [1]
# for i12 in np.arange(1,6,1):     
        # for i16 in np.arange(10,50,10):
rbs_vshift = 10
for i12 in vals:
        for i16 in vals2:
                filename12 = './params/na12annaTFHH2.txt' ##12HH params file that you will update with values below in changesna12
                filename16 = './params/na16HH_TF2.txt' ##16HH params file that you will update with values below in changesna16
                
                ## 12HH mod file params can be changed below
                changesna12 = {
                        "sh": 8,
                        "tha": -38+rbs_vshift,
                        "qa": 5.41,
                        "Ra": 0.3282,
                        "Rb": 0.1,
                        "thi1": -80+rbs_vshift,#-80,
                        "thi2": -80+rbs_vshift,#-80,
                        "qd": 0.5,
                        "qg": 1.5,
                        "mmin": 0.02,
                        "hmin": 0.01,
                        "Rg": 0.01,
                        "Rd": 0.02657,
                        "thinf": -53+rbs_vshift,
                        "qinf": 7.69,
                        "vhalfs": -60+rbs_vshift,
                        "a0s": 0.0003,
                        "gms": 0.2,
                        "q10": 2,
                        "zetas": 12,
                        "smax": 10,
                        "vvh": -58,
                        "vvs": 2,
                        "ar2": 1,
                        "Ena": 55,
                        }
                
           
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
                
                for config_name, config in config_dict.items():
                  path = f'3-e1211k-{config_name}'
                  simwt = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                              ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =3,node_na = 1,
                                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                              plots_folder = f'{root_path_out}/{path}', update=True)
                  # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                  wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = config) #sim_config for changing regions
                  # simwt.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'12-{i12}_16-{i16}_')
                  simwt.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200)
  #

                  
                  
                  
                  # muts = {"M1879T":{"Rd": 0.02472948284108674, "Rg": 0.00810072606215916, "Rb": 0.08544713385358715, "Ra": 0.10890238330112076, "a0s": 0.0006423540797205711, "gms": 0.03866830963351862, "hmin": 0.008675894668791356, "mmin": 0.016464976166148983, "qinf": 6.4227771028178235, "q10": 2.3479836142873656, "qg": 0.19868538684786108, "qd": 0.593407030890033, "qa1": 6.943814973725613, "smax": 13.719739859300681, "sh": 6.9694152592980005, "thinf": -38.00005145513779, "thi2": -76.45455217377341, "thi1": -77.13950134693465, "tha": -32.01116028066946, "vvs": 1.721347362321242, "vvh": -56.63668278016378, "vhalfs": -45.68806836240869, "zetas": 12.902861976927323},
                  # "R1882Q":{"Rd": 0.024481964640376906, "Rg": 0.011605503102516006, "Rb": 0.07229935770107845, "Ra": 0.2851832763358913, "a0s": 0.0006411068608643278, "gms": 0.017857849547739946, "hmin": 0.007683326030147283, "mmin": 0.027134701568044216, "qinf": 6.737717486083065, "q10": 1.7838507575541245, "qg": 0.9877121323185145, "qd": 0.9310341306485088, "qa1": 6.999365335516058, "smax": 12.107905385024555, "sh": 8.19440965711967, "thinf": -38.017891099575365, "thi2": -70.06292054823714, "thi1": -69.58206019231929, "tha": -22.728187717466998, "vvs": 1.5788525989330573, "vvh": -56.803219564771595, "vhalfs": -52.281817845126355, "zetas": 8.770900184234248},
                  # "R853Q":{"Rd": 0.025865219033482965, "Rg": 0.00016701433691450882, "Rb": 0.08327457108124466, "Ra": 0.16472042490264355, "a0s": 0.0003632764348478859, "gms": 0.03953296206867299, "hmin": 0.01155802829191786, "mmin": 0.024119721361783843, "qinf": 9.811306076290183, "q10": 1.2748613566458495, "qg": 1.4557831042136884, "qd": 0.9560328008535323, "qa1": 6.9892745032011705, "smax": 3.247941531535303, "sh": 6.206959218019985, "thinf": -47.965624776637526, "thi2": -61.565524841891936, "thi1": -71.18393358286494, "tha": -28.2887737644131, "vvs": 0.7925109167899197, "vvh": -51.83709708664579, "vhalfs": -51.736573218462354, "zetas": 13.934461247221499},
                  # "R937C":{"Rd": 0.03610000006036732, "Rg": 0.012890797574713116, "Rb": 0.16868803474885782, "Ra": 0.17378946967695688, "a0s": 0.0004986437976961435, "gms": 0.23461313539953887, "hmin": 0.017197285439470925, "mmin": 0.034192550614929304, "qinf": 7.495511148841521, "q10": 1.6422086535193947, "qg": 0.7628271028125702, "qd": 0.8691808522786286, "qa1": 5.336550555342206, "smax": 0.7187119903320823, "sh": 8.146954781629567, "thinf": -43.295265578912954, "thi2": -69.51389764115665, "thi1": -76.30940513687732, "tha": -34.72147979375246, "vvs": 0.07281032769606632, "vvh": -60.53006172866891, "vhalfs": -48.5789830800391, "zetas": 14.835484412450592},
                  # "E1211K":{"Rd": 0.040014537422804496, "Rg": 0.033824389458044835, "Rb": 0.30370226637467845, "Ra": 0.06722786094303114, "a0s": 2.4934068340389556e-06, "gms": 0.12712246338007743, "hmin": 0.026083969094715394, "mmin": 0.021366954413184105, "qinf": 9.560900244928614, "q10": 1.4817755589779813, "qg": 0.5847075306089664, "qd": 0.03944983890205525, "qa1": 5.4551664479256505, "smax": 14.392386655133446, "sh": 7.500874118815216, "thinf": -47.70962481687513, "thi2": -66.05063726492244, "thi1": -72.77880026346939, "tha": -37.57078713090743, "vvs": 2.2904472238965887, "vvh": -54.72125847010487, "vhalfs": -40.71170108020249, "zetas": 2.1656096624936696}}
                  
                  
                  m1879t = {'Rd': 0.013285, 'Rg': 0.01, 'Rb': 0.1, 'Ra': 0.3282, 'a0s': 0.0003, 'gms': 0.2, 'hmin': 0.01, 'mmin': 0.02, 'qinf': 7.69, 'q10': 2, 'qg': 1.5, 'qd': 0.5, 'qa': 5.41, 'smax': 10, 'sh': 8, 'thinf': -30.2, 'thi2': -57.2, 'thi1': -57.2, 'tha': -22, 'vvs': 2, 'vvh': -58, 'vhalfs': -37.2, 'zetas': 12}
                  e1211k = {'Rd': 0.02657, 'Rg': 0.01, 'Rb': 0.1, 'Ra': 0.3282, 'a0s': 0.0003, 'gms': 0.2, 'hmin': 0.01, 'mmin': 0.02, 'qinf': 7.69, 'q10': 2, 'qg': 1.5, 'qd': 0.5, 'qa': 5.41, 'smax': 10, 'sh': 8, 'thinf': -56.15, 'thi2': -83.15, 'thi1': -83.15, 'tha': -33.6, 'vvs': 2, 'vvh': -58, 'vhalfs': -63.15, 'zetas': 12}
                  modify_dict_file(filename12,e1211k)
                  # for mutname,dict in muts.items():
                  #   print(f"mutname is {mutname}")
                  #   print(f"it's corresponding dictionary is {dict}")
                  #   modify_dict_file(filename12,dict)
                  #   # modify_dict_file(filename16,dict)
                  
                  # ## If you want to plot WT vs het, use this code block. simwt will get wt values, you can change sim to get het/KO 
                  
                  simmut = tf.Na12Model_TF(ais_nav12_fac=12*0.5,ais_nav16_fac=12,nav12=1*0.5,nav16=1.3, somaK=1, KP=25, KT=5,
                                              ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =3,node_na = 1,
                                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                              plots_folder = f'{root_path_out}/{path}', update=True)
                  # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                  # simmut.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'm1879t')
                  simmut.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'{path}')

                # simwt = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                #                             ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =3,node_na = 1,
                #                             na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                #                             na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                             plots_folder = f'{root_path_out}/', update=True)
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                # NeuronModel.chandensities(name = f'{plots_folder}/densities_WT') ##TF uncomment to run function and plot channel densities in axon[0]

                # ##het model
                # sim_het = tf.Na12Model_TF(ais_nav12_fac=6,ais_nav16_fac=12,nav12=0.5,nav16=1.3, somaK=1, KP=25, KT=5,
                #                             ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =3,node_na = 1,
                #                             na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                #                             na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                             plots_folder = f'{root_path_out}/{path}', update=True)
                # # sim_het.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvsHet')
                # # sim_het.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=config,vs_amp=[0.5], fnpre=f'WTvsHET')#sim_config for changing regions
                # sim_het.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'HET')

                # NeuronModel.chandensities(name = f'{plots_folder}/densities_Het') ##TF uncomment to run function and plot channel densities in axon[0]

                ##KO model
                # sim_ko = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12,nav12=0,nav16=1.3, somaK=1, KP=25, KT=5,
                #                             ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =0,node_na = 1,
                #                             na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                #                             na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                             plots_folder = f'{root_path_out}/{path}', update=True)
                # # sim_ko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvsHet')
                # # sim_ko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=config,vs_amp=[0.5], fnpre=f'WTvsKO')#sim_config for changing regions
                # sim_ko.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KO')

                # NeuronModel.chandensities(name = f'{plots_folder}/densities_KO') ##TF uncomment to run function and plot channel densities in axon[0]
    






                ##Plot stim/DVDT stacked fig (just mutant, no comparison)
                # fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                # sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue')
                # plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                # fig_volts.savefig(f'{sim.plot_folder}/1-WT_updateon.pdf') #Change output file path here 

                ##Plot WT vs mut stim/dvdt, FI curve, and mut currentscape.
                # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'12-{i12}_16-{i16}_')
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=200,stim_start=30, sweep_len=200)

                ##Plot WT vs mut stim/dvdt only for ~1-3 APs. Can change sweep length in init_stim in NeuronModelClass.py
                
                # sim_ko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvsKO') 
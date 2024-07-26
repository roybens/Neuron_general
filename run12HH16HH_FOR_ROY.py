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
#                 'section' : 'soma',
#                 'segment' : 0.5,
#                 'section_num': 0,
#                 #'currents' : ['ina','ica','ik'],
#                 'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
#                 #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 #'currents'  : ['ihcn_Ih','ik_SKv3_1','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
#                 'ionic_concentrations' :["cai", "ki", "nai"]
#                 #'ionic_concentrations' :["ki", "nai"]
#                 }
# # 2
# sim_config_ais = {
#                 'section' : 'axon',
#                 'segment' : 0.1,
#                 'section_num': 0,
#                 #'currents' : ['ina','ica','ik'],
#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
#                 'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
#                 #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 #'currents'  : ['ihcn_Ih','ik_SKv3_1','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
#                 #'ionic_concentrations' :["cai", "ki", "nai"]
#                 'ionic_concentrations' :["ki", "nai"]
#                 }
# # 3
# sim_config_basaldend = {
#                 'section' : 'dend',
#                 'segment' : 0.5,
#                 'section_num': 70,
#                 #'currents' : ['ina','ica','ik'],
#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
#                 #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 'currents'  : [], #dend (no Ih, no ik_SKv3_1)
#                 'current_names' : ['Ih','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
#                 #'ionic_concentrations' :["cai", "ki", "nai"]
#                 'ionic_concentrations' :[]
#                 }
# #4
# sim_config_nexus = {
#                 'section' : 'apic',
#                 'segment' : 0,
#                 'section_num': 77,
#                 #'currents' : ['ina','ica','ik'],
#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
#                 'currents'  : ['ik_SKv3_1'], #Nexus
#                 #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                
#                 'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
#                 #'ionic_concentrations' :["cai", "ki", "nai"]
#                 'ionic_concentrations' :["ki", "nai"]
#                 }
# #5
# sim_config_apicaldend = {
#                 'section' : 'apic',
#                 'segment' : 0.5,
#                 'section_num': 90,
#                 # 'currents' : ['ina','ica','ik'],
#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
#                 'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ik_SKv3_1','ihcn_Ih'], #AIS (no Ih)
#                 #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 #'currents'  : ['ihcn_Ih','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 # 'ionic_concentrations' :["cai", "ki", "nai"]
#                 'ionic_concentrations' :["ki", "nai"]
#                 }
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


root_path_out = './Plots/12HH16HH_RBS/HH_mutants' ##path for saving your plots
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
                
                
                path = '3-modified_for_trafficking'
                config = sim_config_soma

                simwt = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                            ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =3,node_na = 1,
                                            na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                            na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                            plots_folder = f'{root_path_out}/{path}', update=True)
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = config) #sim_config for changing regions


                
                
                
                muts = {"R379H":{"Rd": 0.033735142839411265, "Rg": 0.010571941586998748, "Rb": 0.10360627837934142, "Ra": 0.3211878521298314, "a0s": 0.000302893756143202, "gms": 0.22470212999085648, "hmin": 0.005882288266423438, "mmin": 0.02, "qinf": 7.912517919079045, "q10": 1.0663032529331906, "qg": 1.531326348990536, "qd": 0.4773793197666614, "qa1": 5.528668503703014, "smax": 11.776406350220551, "sh": 7.016387423656431, "thinf": -42.99883166737607, "thi2": -69.20791872126813, "thi1": -73.21598202141958, "tha": -28.158305428116886, "vvs": 1.6142834147123526, "vvh": -55.866525705893544, "vhalfs": -49.4670216561234, "zetas": 12.034262258064004, "gbar": 0.0782205675472028},
                "T400R":{"Rd": 0.01795240638647841, "Rg": 0.00895062080981376, "Rb": 0.09760640799859088, "Ra": 0.3404938525991082, "a0s": 0.0006272913978461526, "gms": 0.2947154137792179, "hmin": 0.006406697219678107, "mmin": 0.014434339834334481, "qinf": 8.993808687162094, "q10": 1.9711691108758083, "qg": 1.8890898779745864, "qd": 0.7718080464293328, "qa1": 6.769453840150117, "smax": 12.491975660801426, "sh": 7.762324517703443, "thinf": -45.23139963091731, "thi2": -74.93951719607598, "thi1": -69.89199582720104, "tha": -24.975630655786077, "vvs": 2.5285787140479425, "vvh": -54.03332625798278, "vhalfs": -48.78486210473616, "zetas": 10.2427552196792, "gbar": 0.08887910476100962},
                "R853Q":{"Rd": 0.043483853310788544, "Rg": 0.004084270493152188, "Rb": 0.07049663757358686, "Ra": 0.2611336245159532, "a0s": 0.000259733149245198, "gms": 0.1493149577202093, "hmin": 0.010674115528720942, "mmin": 0.005216194110776869, "qinf": 9.7103784662822, "q10": 1.266442764413887, "qg": 0.8673585182979149, "qd": 0.3206013842998041, "qa1": 6.433127566618472, "smax": 9.459897735945667, "sh": 8.491725349353729, "thinf": -47.78646780307593, "thi2": -61.850035077437155, "thi1": -62.17247172970388, "tha": -28.88471496509359, "vvs": 2.7631979926732937, "vvh": -54.282522775377934, "vhalfs": -47.09351573258259, "zetas": 11.160387081267759, "gbar": 0.06231992735925436},
                "R937C":{"Rd": 0.03372072690056526, "Rg": 0.008660944200923051, "Rb": 0.10027757867907665, "Ra": 0.27644460498715173, "a0s": 0.00044216690045375547, "gms": 0.1800939447937904, "hmin": 0.002942269001824107, "mmin": 0.025593111168795042, "qinf": 8.650614005248912, "q10": 2.247231090324812, "qg": 1.4181430933619275, "qd": 0.5265136989401384, "qa1": 5.456050989787319, "smax": 10.396607241093276, "sh": 6.601173898769215, "thinf": -42.998434225844896, "thi2": -66.67042082406887, "thi1": -69.03676111203612, "tha": -28.246181010985385, "vvs": 2.7510572113308456, "vvh": -57.79491892835214, "vhalfs": -49.2786828028931, "zetas": 4.186764763722303, "gbar": 0.05845831874503385},
                "E1211K":{"Rd": 0.03251242077993872, "Rg": 0.013839284424127286, "Rb": 0.16715180086730128, "Ra": 0.17478280457496947, "a0s": 0.0004206454233923332, "gms": 0.3006927793392133, "hmin": 0.00018873975166923244, "mmin": 0.009393756262, "qinf": 9.926065471417127, "q10": 1.444808156675999, "qg": 1.5106170709616464, "qd": 0.7710303803793445, "qa1": 4.7751589212132695, "smax": 8.40619555147451, "sh": 7.2569965721902685, "thinf": -47.992797751942504, "thi2": -72.59874782819409, "thi1": -69.27453716606385, "tha": -33.5545841699252, "vvs": 0.3531404126525447, "vvh": -55.54942264466725, "vhalfs": -51.86961685346286, "zetas": 11.356414843898834, "gbar": 0.06265679238921772},
                "K1422E":{"Rd": 0.044268558136772954, "Rg": 0.009972866665400579, "Rb": 0.11182312970291847, "Ra": 0.21716241346378895, "a0s": 3.497158333838621e-05, "gms": 0.22618844083367776, "hmin": 0.005887566631530394, "mmin": 0.02180279802639355, "qinf": 9.808401513713434, "q10": 2.278793771321614, "qg": 1.8004765031649959, "qd": 0.6565081184177535, "qa1": 5.482812768816002, "smax": 10.527882489068931, "sh": 8.214720650147811, "thinf": -47.89494542473024, "thi2": -73.98917176466045, "thi1": -72.00398445547816, "tha": -30.61751189740822, "vvs": 1.7517354901748887, "vvh": -55.48706773825774, "vhalfs": -47.70581344299175, "zetas": 9.655998715937317, "gbar": 0.07972935049799376},
                "M1879T":{"Rd": 0.024731587510977145, "Rg": 0.013184842765324056, "Rb": 0.037011497119045215, "Ra": 0.2231942081522566, "a0s": 8.416855939504312e-05, "gms": 0.11812074790023197, "hmin": 0.020028259141849244, "mmin": 0.024383441731317262, "qinf": 5.979264030521502, "q10": 2.3784235930496496, "qg": 1.371540693133289, "qd": 0.42193041006432286, "qa1": 6.970114071056039, "smax": 13.388579909617759, "sh": 6.025674640542583, "thinf": -38.01958282203517, "thi2": -69.62294593648446, "thi1": -66.75389162190581, "tha": -21.502764762860544, "vvs": 1.796486367478632, "vvh": -53.4800297064406, "vhalfs": -48.1670570647453, "zetas": 11.170829164649744, "gbar": 0.06527992471363205},
                "R1882Q":{"Rd": 0.02051744819459416, "Rg": 0.009211114919054318, "Rb": 0.058043800028580894, "Ra": 0.2784076410381933, "a0s": 0.00010079870798486245, "gms": 0.3004063653533408, "hmin": 0.01793393920916245, "mmin": 0.03894863626552881, "qinf": 6.0366658684659615, "q10": 2.4831459499252477, "qg": 0.9730838898087506, "qd": 0.5455432247815544, "qa1": 6.615421896947292, "smax": 9.557798880178659, "sh": 9.445040348834937, "thinf": -38.005780736573165, "thi2": -72.60387928598942, "thi1": -74.3494263473455, "tha": -24.195136615680386, "vvs": 1.8921025779292115, "vvh": -59.23439770665602, "vhalfs": -45.101859814795134, "zetas": 6.261298718928709, "gbar": 0.12826942804169128},
                "F257I":{"Rd": 0.03142983561122226, "Rg": 0.008742762941160328, "Rb": 0.09996943517122887, "Ra": 0.29490893605916685, "a0s": 0.0002463735449592615, "gms": 0.29547828762484485, "hmin": 0.010522463371275827, "mmin": 0.02313631398400879, "qinf": 7.123904286441568, "q10": 1.203835923980804, "qg": 1.5228227713091373, "qd": 0.20997466241174556, "qa1": 6.745976653714254, "smax": 12.881757185151999, "sh": 8.248846290128233, "thinf": -38.059870605731824, "thi2": -78.13997433430988, "thi1": -69.07591907688773, "tha": -26.769871816791074, "vvs": 2.8499163350528045, "vvh": -52.84680006170201, "vhalfs": -45.58251705671013, "zetas": 10.727004127568978, "gbar": 0.0895266007678103},
                "K1480E":{"Rd": 0.022609634479151035, "Rg": 0.004062218988095459, "Rb": 0.05666200306371379, "Ra": 0.3490895630208899, "a0s": 0.0004429799838899641, "gms": 0.18214086753475883, "hmin": 0.019884701455781688, "mmin": 0.02712528022824949, "qinf": 8.13240389286693, "q10": 2.2946290280156076, "qg": 1.5793122504065287, "qd": 0.24796584236475022, "qa1": 6.932036722338341, "smax": 12.573358082442416, "sh": 7.989581373470089, "thinf": -39.24794027442662, "thi2": -72.52935167322642, "thi1": -67.7503248602702, "tha": -19.049271689816102, "vvs": 2.5745453904584643, "vvh": -57.965341348225316, "vhalfs": -57.860337314359114, "zetas": 4.468397502225563, "gbar": 0.0792249373067178}}
                
                
               

                for mutname,dict in muts.items():
                  print(f"mutname is {mutname}")
                  print(f"it's corresponding dictionary is {dict}")
                  modify_dict_file(filename12,dict)
                  # modify_dict_file(filename16,dict)
                
                ## If you want to plot WT vs het, use this code block. simwt will get wt values, you can change sim to get het/KO 
                
                  simmut = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                              ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =3,node_na = 1,
                                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                              plots_folder = f'{root_path_out}/{path}', update=True)
                  # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                  simmut.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'{mutname}')

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
                # sim_het.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=config,vs_amp=[0.5], fnpre=f'WTvsHET')#sim_config for changing regions
                # # NeuronModel.chandensities(name = f'{plots_folder}/densities_Het') ##TF uncomment to run function and plot channel densities in axon[0]

                # ##KO model
                # sim_ko = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12,nav12=0,nav16=1.3, somaK=1, KP=25, KT=5,
                #                             ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =0,node_na = 1,
                #                             na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                #                             na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                             plots_folder = f'{root_path_out}/{path}', update=True)
                # # sim_ko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvsHet')
                # sim_ko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=config,vs_amp=[0.5], fnpre=f'WTvsKO')#sim_config for changing regions
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
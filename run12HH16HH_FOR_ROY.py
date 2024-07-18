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


root_path_out = './Plots/12HH16HH_RBS' ##path for saving your plots
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
                        #"ena": 55
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
                
                ##Functions to update params files with values entered above (rather than having to change the params file names). Comment out if you don't want any updating.
                modify_dict_file(filename12, changesna12)
                modify_dict_file(filename16, changesna16)

                ##Run the sim for a single mutant (no comparison)
                # sim = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=2,nav12=3,nav16=1, somaK=1, KP=100, KT=10,
                #                         ais_ca = 1,ais_Kca = 1,soma_na16=1,soma_na12 = 1,node_na = 1,
                #                 na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/1', #Change output file path here 
                #                 pfx=f'WT_', update=True) 
               
                
                # ##Plot stim/DVDT stacked fig
                # fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                # sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue')
                # plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                # fig_volts.savefig(f'{sim.plot_folder}/1.pdf') #Change output file path here 

                # #Plot currentscape
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=200,stim_start=30, sweep_len=200)


                
                ## If you want to plot WT vs het, use this code block. simwt will get wt values, you can change sim to get het/KO 
                plots_folder = f'{root_path_out}/2-TEST'
                simwt = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12,nav12=1,nav16=1.3, somaK=1, KP=25, KT=5,
                                            ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =3,node_na = 1,
                                            na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                            na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                            plots_folder = f'{root_path_out}/2-TEST', update=True)
                wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                NeuronModel.chandensities(name = f'{plots_folder}/densities_WT') ##TF uncomment to run function and plot channel densities in axon[0]

                ##het model
                sim_het = tf.Na12Model_TF(ais_nav12_fac=6,ais_nav16_fac=12,nav12=0.5,nav16=1.3, somaK=1, KP=25, KT=5,
                                            ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =3,node_na = 1,
                                            na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                            na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                            plots_folder = f'{root_path_out}/2-TEST', update=True)
                sim_het.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvsHet')
                NeuronModel.chandensities(name = f'{plots_folder}/densities_Het') ##TF uncomment to run function and plot channel densities in axon[0]

                ##KO model
                sim_ko = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=12,nav12=0,nav16=1.3, somaK=1, KP=25, KT=5,
                                            ais_ca = 100,ais_Kca = 0.5,soma_na16=0.8,soma_na12 =0,node_na = 1,
                                            na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                            na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                            plots_folder = f'{root_path_out}/2-TEST', update=True)
                NeuronModel.chandensities(name = f'{plots_folder}/densities_KO') ##TF uncomment to run function and plot channel densities in axon[0]
    

                ##Plot stim/DVDT stacked fig (just mutant, no comparison)
                # fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                # sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue')
                # plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                # fig_volts.savefig(f'{sim.plot_folder}/1-WT_updateon.pdf') #Change output file path here 

                ##Plot WT vs mut stim/dvdt, FI curve, and mut currentscape.
                # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'12-{i12}_16-{i16}_')
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=200,stim_start=30, sweep_len=200)

                ##Plot WT vs mut stim/dvdt only for ~1-3 APs. Can change sweep length in init_stim in NeuronModelClass.py
                
                sim_ko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvsKO') 
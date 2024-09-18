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


config_dict3={"sim_config_soma": sim_config_soma}

for config_name, config in config_dict3.items():
  path = f'35-Incrementplots_kevin'


# for factor in [0.00001,0.0001,0.001,0.01,0.1,0.25,0.5,0.75,1,1.2,2,4,6,10,25,50,100,1000,10000,100000]:
# for amps in np.arange(-0.4,0.4,0.05):


# for factor in [1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]:

# fig,axs = plt.subplots(1,1)
fig, axs = plt.subplots(figsize=(cm_to_in(8), cm_to_in(8)))
cmap = cm.get_cmap('rainbow')
# for i, factor in enumerate([1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0]):
for i, factor in enumerate([0]):

  ## WT vs HET vs Mut  
  ##WT model
  simwt = tf.Na12Model_TF(ais_nav12_fac=12,ais_nav16_fac=12*factor,nav12=1,nav16=1.3*factor, somaK=1*2.2*0.01, KP=25*0.15, KT=5,
                              ais_ca = 100*8.6*0.1,ais_Kca = 0.5,soma_na16=1*factor,soma_na12=3.2,node_na = 1,
                              na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                              na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                              plots_folder = f'{root_path_out}/{path}', update=True, fac=None)
  Vm,_,t,_ = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = config) #stim_amp=0.5

  # fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
  # simwt.plot_stim(axs = axs[0],stim_amp = 0.3,dt=0.005, clr='cadetblue')
  # plot_dvdt_from_volts(simwt.volt_soma, simwt.dt, axs[1],clr='cadetblue')
  # fig_volts.savefig(f'{simwt.plot_folder}/16-{factor}.pdf') #Change output file path here 

  dvdt = np.gradient(Vm)/0.005
  color = cmap(i/11)
  axs.plot(Vm[1:25000],dvdt[1:25000],color=color, alpha=0.8,linewidth=1)
out = f'{root_path_out}/{path}/dvdt_16-2.pdf'
# axs.legend()  # Add a legend to the plot
fig.savefig(out)
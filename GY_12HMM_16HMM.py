
#coppied from RBS Clean TF
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
import Document as doc
import Tim_ng_functions as nf

sim_config_soma = {
                'section' : 'soma',
                'segment' : 0.5,
                'section_num': 0,
                #'currents' : ['ina','ica','ik'],
                'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
                #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
                #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                #'currents'  : ['ihcn_Ih','ik_SKv3_1','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
                'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
                'ionic_concentrations' :["cai", "ki", "nai"]
                #'ionic_concentrations' :["ki", "nai"]
                }


#   Modifies values in a dictionary stored in a text file.
def modify_dict_file(filename, changes):
#   Args:filename: The name of the text file containing the dictionary.
#       changes: A dictionary containing key-value pairs where the key is the key to modify in the original dictionary and the value is the new value.

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



# root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/Restart030824/6-HMM_focusonTTP_042624/10-12HMMmuts_fitto_1012TTP8_050824'
root_path_out = './Plots/12HMM_16HMM_GY/mature'

if not os.path.exists(root_path_out):
        os.makedirs(root_path_out)
        #os.mkdir(root_path_out)



##Adding below function to loop through different na16.mod params        
# filename = "/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TF100923-2.txt" ##TF031524 for changing 8st na12
filename12 = './params/na12_HMM_TEMP_PARAMS.txt'
filename16 = './params/na16_HMM_TEMP_PARAMS.txt'


                

## Best 12 and 16 params as of 072224
## THE LATEST R850P MUTANT was made with WT :TF060324 (same as na12_HMM_TF050724) WT params 
changesna12_060324 = {"a1_0": 62.774771313021546,"a1_1": 0.6854152336583206,"b1_0": 3.2117067311143277,"b1_1": 0.1432460480232296, "a2_0": 2468.966900014909,"a2_1": 0.0834387238328, "b2_0": 490.16060600231606,"b2_1": 2.969500725999265,"a3_0": 190.5883640336242,"a3_1": 0.003108395956123883,"b3_0": 7689.251014289831, "b3_1": 0.04054164070835632,"bh_0": 4.063594186259147,"bh_1": 2.115884898210715, "bh_2": 0.1433653421971472,"ah_0": 1.3563238605774417,"ah_1": 6568.351916792737, "ah_2": 0.011127551783912584,"vShift": -18.276678986708095, "vShift_inact": 16.74204011921361, "maxrate": 6.170113221706686}                
changesna16_071624best={"a1_0": 86.82768844997113, "a1_1": 0.12481160483736764, "b1_0": 0.03636308557245105, "b1_1": 0.07299197117480938, "a2_0": 5870.594264277059, "a2_1": 0.20381201621527256, "b2_0": 445.51379959201944, "b2_1": 0.014057437484476853, "a3_0": 1549.7689816436775, "a3_1": 0.08223497094200147, "b3_0": 460.3178077224841, "b3_1": 0.010814365773659428, "bh_0": 13.70152920233826, "bh_1": 9.233117481911744, "bh_2": 0.05775463093748526, "ah_0": 0.7125397402558968, "ah_1": 52695.59895637044, "ah_2": 0.07354314395481377, "vShift": -9.512610605026387, "vShift_inact": 17.512316086445306, "maxrate": 13.917366173297317}

#For mature model
modify_dict_file(filename12, changesna12_060324)
modify_dict_file(filename16, changesna16_071624best)

"""# For Seveloping model, replacing the Nav1.6 with Nav1.2 WT
modify_dict_file(filename12, changesna12_060324)
modify_dict_file(filename16, changesna12_060324)
"""

# Developing WT includes only Nav1.2 HMM WT      
simwt = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
              ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
              na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
              na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
              plots_folder = f'{root_path_out}/WT', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)

##Plotting only WT Stim/DVDT and Currentscapes
simwt.make_currentscape_plot(amp=0.5, time1=1000,time2=1075,stim_start=700, sweep_len=1200)       
simwt.make_currentscape_plot(amp=0.5, time1=50,time2=200,stim_start=30, sweep_len=200)  


changesna12 = {"R850P_062724": {'a1_0': 41.24466597259794, 'a1_1': 0.5308501317510134, 'b1_0': 7.386920140708283, 'b1_1': 0.008256767752317935, 'a2_0': 10755.581571569404, 'a2_1': 0.2941534968877462, 'b2_0': 508.5221717496915, 'b2_1': 0.8344607280938177, 'a3_0': 357.34870015416504, 'a3_1': 0.0002195891536895594, 'b3_0': 1070.0986194771494, 'b3_1': 0.027183145081577945, 'bh_0': 3.7310446112469187, 'bh_1': 11.870394633074387, 'bh_2': 0.11998196950856949, 'ah_0': 11.265619816992157, 'ah_1': 711379.2077178769, 'ah_2': 0.0020378247251452777, 'vShift': -9.743154184024819, 'vShift_inact': 0.4138496607777782, 'maxrate': 10.159989993015305}}
    
for mutname,dict in changesna12.items():
    #for one mut: still use this for loop beacuse the mutname is being used
    print(f"mutname is {mutname}")
    print(f"it's corresponding dictionary is {dict}")
    nf.modify_dict_file(filename12,dict)
    #nf.modify_dict_file(filename16,changesna12)
    # In case of developing we have two options: 1. Het: two Nav1.2 mutants + two Nav1.2 WT
    # 2. Hom: four Nav1.2 mutant


    sim = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
              ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
              na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
              na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
              plots_folder = f'{root_path_out}/Hom_{mutname}', pfx=f'WT_', update=True)
                        
                        
                                        
    fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
    sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
    plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
    fig_volts.savefig(f'{sim.plot_folder}/hom_{mutname}.pdf')

    sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KO')
    sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)
    sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1075,stim_start=700, sweep_len=1200)
    


















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
root_path_out = './Plots/12HMM16HMM/26_confirmWT'

if not os.path.exists(root_path_out):
        os.makedirs(root_path_out)
        # os.mkdir(root_path_out)



##Adding below function to loop through different na16.mod params        
# filename = "/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TF100923-2.txt" ##TF031524 for changing 8st na12
filename12 = './params/na12_HMM_TEMP_PARAMS.txt'
filename16 = './params/na16_HMM_TEMP_PARAMS.txt'


                

## Best 12 and 16 params as of 072224
changesna12_071824best ={"a1_0": 3.1547345527269233, "a1_1": 0.05510300665105835, "b1_0": 4.791955661615136, "b1_1": 0.09014477225513692, "a2_0": 3015.155056494468, "a2_1": 0.30987923885393026, "b2_0": 919.3139955076967, "b2_1": 0.41962767235919507, "a3_0": 109.85728965102251, "a3_1": 0.24852254942384186, "b3_0": 1712.2193773613558, "b3_1": 0.01912898529951851, "bh_0": 8.027353908819931, "bh_1": 8.174548719738821, "bh_2": 0.11446203713204262, "ah_0": 0.06601487564289754, "ah_1": 405124.7535686269, "ah_2": 0.08651802346109899, "vShift": -23.438854488000004, "vShift_inact": 15.461948540212093, "maxrate": 11.685304243202804}
changesna16_071624best={"a1_0": 86.82768844997113, "a1_1": 0.12481160483736764, "b1_0": 0.03636308557245105, "b1_1": 0.07299197117480938, "a2_0": 5870.594264277059, "a2_1": 0.20381201621527256, "b2_0": 445.51379959201944, "b2_1": 0.014057437484476853, "a3_0": 1549.7689816436775, "a3_1": 0.08223497094200147, "b3_0": 460.3178077224841, "b3_1": 0.010814365773659428, "bh_0": 13.70152920233826, "bh_1": 9.233117481911744, "bh_2": 0.05775463093748526, "ah_0": 0.7125397402558968, "ah_1": 52695.59895637044, "ah_2": 0.07354314395481377, "vShift": -9.512610605026387, "vShift_inact": 17.512316086445306, "maxrate": 13.917366173297317}

modify_dict_file(filename12, changesna12_071824best)
modify_dict_file(filename16, changesna16_071624best)

simwt = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
                plots_folder = f'{root_path_out}/', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)

# fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
# simwt.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
# plot_dvdt_from_volts(simwt.volt_soma, simwt.dt, axs[1],clr='cadetblue')
# fig_volts.savefig(f'{simwt.plot_folder}/WT.pdf')


## vshifted hmm fits to move 17 to the right (couldn't tune 082924)
# vshift = {"mut24_n2_shift17":{"a1_0": 44.20762460304075, "a1_1": 0.22904908195227058, "b1_0": 1.0895620045511527, "b1_1": 0.10645926360864319, "a2_0": 10631.6923307076, "a2_1": 0.31471555894152037, "b2_0": 297.8002288303858, "b2_1": 4.330759483800555, "a3_0": 142.14741791584726, "a3_1": 0.02712756421974758, "b3_0": 3388.2302536952952, "b3_1": 0.00444433148682701, "bh_0": 3.6507619283095227, "bh_1": 12.068955126311407, "bh_2": 0.14232122859033564, "ah_0": 4.962768758570474, "ah_1": 347377.78057155677, "ah_2": 0.06423396770148165, "vShift": -14.486966709305836, "vShift_inact": 3.4639274170146033, "maxrate": 6898.9860247926445},
# "mut234_n2_shift17":{"a1_0": 32.85040930843276, "a1_1": 1.6615046528718203, "b1_0": 1.1283135428527846, "b1_1": 0.11913312637809705, "a2_0": 5420.596370431161, "a2_1": 0.03662723327331317, "b2_0": 241.75069020862716, "b2_1": 2.8544275072402634, "a3_0": 175.65588800727284, "a3_1": 0.039417295653628406, "b3_0": 1567.4631041099394, "b3_1": 0.051773724586163694, "bh_0": 3.2239491868838086, "bh_1": 1.622849827710409, "bh_2": 0.17484029977300872, "ah_0": 14.341962154480752, "ah_1": 66673.98417663306, "ah_2": 0.022747115382984594, "vShift": -20.063244751830126, "vShift_inact": 11.310700688405518, "maxrate": 1302.2771696885973}}


# for name, mut in vshift.items():
# for mutname,dict in vshift.items():
#   print(f"mutname is {mutname}")
#   print(f"it's corresponding dictionary is {dict}")
#   modify_dict_file(filename12,dict)
# #   # modify_dict_file(filename16,dict)

#   root_path_out = f'./Plots/12HMM16HMM/25_scanVshiftFits/{mutname}'

#   if not os.path.exists(root_path_out):
#           os.makedirs(root_path_out)
        
  # simwt = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
  #               ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
  #               na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
  #               na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
  #               plots_folder = f'{root_path_out}/', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
  # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)

# ##Plotting only WT Stim/DVDT and Currentscapes
# fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
# simwt.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
# plot_dvdt_from_volts(simwt.volt_soma, simwt.dt, axs[1],clr='cadetblue')
# fig_volts.savefig(f'{simwt.plot_folder}/WT.pdf')

##Get states of HMM (plot_8states in NeuronModelClass.py)
# fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
# ap_t, vm_t = simwt.plot_stim(axs=axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
# nf.plot_8states(csv_name="./Plots/Channel_state_plots/na12_channel_states.csv", outfile_sfx="na12_072924",start = 27500,stop=30000,ap_t=ap_t, vm_t=vm_t )
# nf.plot_8states(csv_name="./Plots/Channel_state_plots/na16_channel_states.csv", outfile_sfx="na16_072924",start = 27500,stop=30000,ap_t=ap_t, vm_t=vm_t )

# simwt.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200)  
# simwt.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WT_',wt_fi = [0, 0, 3, 7, 9, 10, 10, 11, 12, 12, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 18])#fnpre=f'{mutTXT}')

# simwt.make_currentscape_plot(amp=0.5, time1=100,time2=400,stim_start=100, sweep_len=800)
# simwt.make_currentscape_plot(amp=0.5, time1=50,time2=200,stim_start=30, sweep_len=200)  




# ## Testing if I can change vshift and vshift_inact to move threshold +17
# na12_vshift17 ={"a1_0": 3.1547345527269233, "a1_1": 0.05510300665105835, "b1_0": 4.791955661615136, "b1_1": 0.09014477225513692, "a2_0": 3015.155056494468, "a2_1": 0.30987923885393026, "b2_0": 919.3139955076967, "b2_1": 0.41962767235919507, "a3_0": 109.85728965102251, "a3_1": 0.24852254942384186, "b3_0": 1712.2193773613558, "b3_1": 0.01912898529951851, "bh_0": 8.027353908819931, "bh_1": 8.174548719738821, "bh_2": 0.11446203713204262, "ah_0": 0.06601487564289754, "ah_1": 405124.7535686269, "ah_2": 0.08651802346109899, "vShift": -6.438854488000004, "vShift_inact": 32.461948540212093, "maxrate": 11.685304243202804}
# na16_vshift17={"a1_0": 86.82768844997113, "a1_1": 0.12481160483736764, "b1_0": 0.03636308557245105, "b1_1": 0.07299197117480938, "a2_0": 5870.594264277059, "a2_1": 0.20381201621527256, "b2_0": 445.51379959201944, "b2_1": 0.014057437484476853, "a3_0": 1549.7689816436775, "a3_1": 0.08223497094200147, "b3_0": 460.3178077224841, "b3_1": 0.010814365773659428, "bh_0": 13.70152920233826, "bh_1": 9.233117481911744, "bh_2": 0.05775463093748526, "ah_0": 0.7125397402558968, "ah_1": 52695.59895637044, "ah_2": 0.07354314395481377, "vShift": 8.512610605026387, "vShift_inact": 34.512316086445306, "maxrate": 13.917366173297317}
# modify_dict_file(filename12, na12_vshift17)
# modify_dict_file(filename16, na16_vshift17)
# #####



# fac=1
# for fac in (0.01,0.1,0.25,0.5,2,4,10,50,100):
for fac in (0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18):
# for fac in (3.565, 3.57, 3.58, 3.59):
# for fac in (0.0001,0.001,0.01):
# for fac in (1.5,1.75,2.25,2.5,2.75,3,3.25,3.5,3.56):
# for fac in (2.5,3):
# for fac in (5,10,15):

  simtim = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56*fac, KT=10, #nav12=3*2*1.5
                                      ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/wt-KP', 
                                      pfx=f'{str(fac)}', update=True)
  simtim.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'wt-KP-{str(fac)}')
# simtim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KO_',wt_fi = [0, 0, 1, 2, 5, 8, 9, 10, 11, 12, 12, 13, 13, 14, 14, 14, 15, 15, 15, 17, 17])#fnpre=f'{mutTXT}')
# simtim.make_currentscape_plot(amp=0.5, time1=50,time2=200,stim_start=30, sweep_len=200)  
  
# simhet = tf.Na12Model_TF(ais_nav12_fac=(2*100)/2,ais_nav16_fac=10*4,nav12=(3*3)/2,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
#                                     ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
#                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
#                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
#                                     params_folder='./params/', plots_folder=f'{root_path_out}/24-longsweep_wthetko', 
#                                     pfx=f'{str(fac)}', update=True)
# simhet.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'het-{str(fac)}')
# simhet.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'HET_',wt_fi = [0, 0, 3, 7, 9, 10, 10, 11, 12, 12, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 18])#fnpre=f'{mutTXT}')


# simko = tf.Na12Model_TF(ais_nav12_fac=(2*100)*0,ais_nav16_fac=10*4,nav12=(3*3)*0,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
#                                     ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
#                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
#                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
#                                     params_folder='./params/', plots_folder=f'{root_path_out}/24-longsweep_wthetko', 
#                                     pfx=f'{str(fac)}', update=True)
# simko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ko-{str(fac)}')
# simko.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KO_',wt_fi = [0, 0, 3, 7, 9, 10, 10, 11, 12, 12, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 18])#fnpre=f'{mutTXT}')



  '''
  # somaK Iteration
  sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25*fac, KP=1000*3.56, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_somaK{str(fac)}', update=True)
  sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac-{str(fac)}')

  # KT Iteration
  sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10*fac,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_KT{str(fac)}', update=True)
  sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac-{str(fac)}')

  # ais_Kca Iteration
  sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_ais_Kca{str(fac)}', update=True)
  sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac-{str(fac)}')

  sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56*fac, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_KP{str(fac)}', update=True)
  sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac-{str(fac)}')

  # ais_nav12_fac Iteration
  sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*100*fac,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_ais_nav12_fac{str(fac)}', update=True)
  sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac-{str(fac)}')

  # ais_nav16_fac Iteration
  sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*fac,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_ais_nav16_fac{str(fac)}', update=True)
  sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac-{str(fac)}')

  # nav12 Iteration
  sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3*fac,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_nav12{str(fac)}', update=True)
  sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac-{str(fac)}')

  # nav16 Iteration
  sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5*fac, somaK=50*0.25, KP=1000*3.56, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_nav16{str(fac)}', update=True)
  sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac-{str(fac)}')

  # soma_na12 Iteration
  sim_test_soma_na12 = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5*fac, soma_na16=1, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_soma_na12{str(fac)}', update=True)
  sim_test_soma_na12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na12_fac-{str(fac)}')

  # soma_na16 Iteration
  sim_test_soma_na16 = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1*fac, dend_nav12=1, node_na=1,
                                na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                pfx=f'WT_soma_na16{str(fac)}', update=True)
  sim_test_soma_na16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na16_fac-{str(fac)}')
  '''  






'''
    sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1*fac, KP=1000, KT=10,
                                     ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                     pfx=f'WT_somaK_fac{str(fac)}', update=True)
    sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac{str(fac)}')

    # KT Iteration
    sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10*fac,
                                  ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KT_fac{str(fac)}', update=True)
    sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac{str(fac)}')


    # ais_Kca Iteration
    sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                       ais_ca = 100,ais_Kca = 5*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                       na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                       na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                       params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                       pfx=f'WT_ais_Kca{str(fac)}', update=True)
    sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac{str(fac)}')

    sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                    na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                    na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_KP{str(fac)}', update=True)
    sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac{str(fac)}')
        



# soma_na12 Iteration
    sim_test_soma_na12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5*fac, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_soma_na12{str(fac)}', update=True)
    sim_test_soma_na12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na12_fac{str(fac)}')

    # soma_na16 Iteration
    sim_test_soma_na16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1*fac, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_soma_na16{str(fac)}', update=True)
    sim_test_soma_na16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na16_fac{str(fac)}')

    
    sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3*fac,nav16=7.5, somaK=1, KP=1000, KT=10,
                                     ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                     pfx=f'WT_nav12_fac{str(fac)}', update=True)
    sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac{str(fac)}')

    # nav16 Iteration
    sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5*fac, somaK=1, KP=1000, KT=10,
                                     ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                     pfx=f'WT_nav16_fac{str(fac)}', update=True)
    sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac{str(fac)}')

    

    sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*fac,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                              ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                              na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                              na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                              params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav12_fac{str(fac)}', update=True)
    sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac{str(fac)}')

    # ais_nav16_fac Iteration
    sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*fac,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                            ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                            na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                            na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                            params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav16_fac{str(fac)}', update=True)
    sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac{str(fac)}')




# somaK Iteration
    sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1*fac, KP=1000, KT=10,
                                     ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                     pfx=f'WT_somaK_fac{str(fac)}', update=True)
    sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac{str(fac)}')

    # KT Iteration
    sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10*fac,
                                  ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KT_fac{str(fac)}', update=True)
    sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac{str(fac)}')

    # ais_ca Iteration
    sim_test_ais_ca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                      ais_ca = 100*fac,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                      pfx=f'WT_ais_ca_fac{str(fac)}', update=True)
    sim_test_ais_ca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_ca_fac{str(fac)}')

    # ais_Kca Iteration
    sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                       ais_ca = 100,ais_Kca = 5*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                       na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                       na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                       params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                       pfx=f'WT_ais_Kca_fac{str(fac)}', update=True)
    sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac{str(fac)}')
'''

'''   
        sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*fac,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                                ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                                params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav12_fac{str(fac)}', update=True)
        sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac{str(fac)}')

        # ais_nav16_fac Iteration
        sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*fac,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                                ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                                params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav16_fac{str(fac)}', update=True)
        sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac{str(fac)}')

        # nav12 Iteration
        sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3*fac,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_nav12{str(fac)}', update=True)
        sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac{str(fac)}')

        # nav16 Iteration
        sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5*fac, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_nav16{str(fac)}', update=True)
        sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac{str(fac)}')

        # KP Iteration
        sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                    na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                    na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_KP{str(fac)}', update=True)
        sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac{str(fac)}')
        

'''
















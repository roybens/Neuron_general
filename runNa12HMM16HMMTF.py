# import Na12Model_TF as tf
# import matplotlib.pyplot as plt
# import numpy as np
# import NrnHelper as NH
# from neuron import h


# #sim.make_hmm_wt()
# #fig, ficurveax = plt.subplots(1, 1)
# print('start')
# sim = tf.Na12Model_TF()
# print('first')

# sim.plot_stim(axs = axs_volts,dt=0.1,stim_amp = 0.5,rec_extra = True,)
# print('done')
# #sim.plot_stim()

#import Developing_12HMM as dev
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

#_____________For Looping through mutants________________________________________________________________________
# for i in range(1,13):
#         for j in range(1,5):
#             mutant = 'mut'+str(i)+'_'+str(j)
#             #mutant = 'test0921'
#             # path = os.path.join(root_path, mutant)
#             # os.mkdir(path)
#             #sim = tf.na12HH16HMM_TF(na12name = 'na12_TF2' , mut_name = 'na12_TF2', na16name = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/{mutant}/')
#             sim = tf.na12HH16HMM_TF(na16name = f'{mutant}_Na16hof',na16mut = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/synth_na16muts_HOMtest/scank/{mutant}/')

#             #sim = tf.na12HH16HMM_TF(na16name = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/{mutant}/')
#             sim_config = {
#                             'section' : 'soma',
#                             'segment' : 0.5,
#                             'section_num': 0,
#                             #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'],
#                             'currents' : ['ina','ica','ik'],
#                             'ionic_concentrations' :["cai", "ki", "nai"]
                            
#                         }
#             current_names = sim_config['currents']
#             Vm, I, t, stim, ionic = sim.make_current_scape(sim_config=sim_config)

#             plot_config = {
#                     "output": {
#                         "savefig": True,
#                         "dir": "./Plots/Currentscape/TEST/",
#                         "fname": "test_plot",
#                         "extension": "pdf",
#                         "dpi": 600,
#                         "transparent": False
#                     },
#                     "current": {"names": current_names},
#                     "ions":{"names": ["ca", "k", "na"]},
#                     "voltage": {"ylim": [-90, 50]},
#                     "legendtextsize": 5,
#                     "adjust": {
#                         "left": 0.15,
#                         "right": 0.8,
#                         "top": 1.0,
#                         "bottom": 0.0
#                         }
#                     }
#             #print(I.keys())
#             #sim.make_current_scape()
#             #sim.plot_stim()
#             # sim.plot_currents()
#             # sim.plot_volts_dvdt()
#             # sim.plot_fi_curve(0,5,20,fn = f'16HMM_muts_TF')
#             #sim.get_axonal_ks()
#             #sim.plot_axonal_ks()

#             #scan12_16(na16name = f'{mutant}_Na16hof',na16mut = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/synth_na16muts_HOMtest/{mutant}/')
#             scanK(na16name = f'{mutant}_Na16hof',na16mut = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/synth_na16muts_HOMtest/{mutant}/')
            
#             #dvdt_all_plot()
#             #print(h.cell.soma.psection())
###___________________________________________________________________________________________________________





################################################################################################################################
        #section[section_num](segment)
        #Section: soma, section_num: 0, segment:0.5 == Middle of Soma
        #Section: axon, section_num:0, segment:0 == AIS
        #Section: dend, section_num: 70, segment: 0.5 == Basal dendrite mid-shaft ***should check this in gui
        #Section: apic, section_num:77, segment:0       77(0) or 66(1)  == Apical Nexus
        #Section: apic, section_num:90, segment:0.5   == Most distal apical dendrite
# sim_config = {
#                 'section' : 'axon',
#                 'segment' : 0.1,
#                 'section_num': 0,

#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
#                 'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
                
#                 # 'currents' : ['ina','ica','ik'],
#                 'ionic_concentrations' :["cai", "ki", "nai"]
                
#             }
# current_names = sim_config['currents']
################################################################################################################################

#Vm, I, t, stim, ionic = sim.make_current_scape(sim_config=sim_config)

# plot_config = {
#         "output": {
#             "savefig": True,
#             "dir": "./Plots/Currentscape/TEST/",
#             "fname": "test_plot",
#             "extension": "pdf",
#             "dpi": 600,
#             "transparent": False
#         },
#         "current": {"names": current_names},
#         "ions":{"names": ["ca", "k", "na"]},
#         "voltage": {"ylim": [-90, 50]},
#         "legendtextsize": 5,
#         "adjust": {
#             "left": 0.15,
#             "right": 0.8,
#             "top": 1.0,
#             "bottom": 0.0
#             }
#         }






#_____________________________Overexpression and TTX experiments__________________________
# overexp(na16name = 'na16mut44_092623',na16mut = 'na16mut44_092623', 
#   plots_folder = f'./Plots/12HH16HMM_TF/100223/{mutant}/')
#rng = [.05,.1,.15,.2]
# rng = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
# for i in rng:
#     ttx(na16name = 'na16mut44_092623',na16mut = 'na16mut44_092623', 
#         plots_folder = f'./Plots/12HH16HMM_TF/100223/{mutant}/ttxWTrange10-100/', wt_factor =i, mut_factor =0,fnpre =f'wt_{i}')
#_________________________________________________________________________________________


##____________Electrophys Feature Extraction Library efel______________________________
# ef.get_sim_volt_values(mutant_name = 'na12_HMM_TF100923')
# ef.get_features(mutant_name = 'na12_HMM_TF100923')


###__________________120523 Experiments synth 12hmm muts__________________________________
# overexp(na16name = 'na16mut44_092623',na16mut = 'na16mut44_092623', 
#   plots_folder = f'./Plots/12HH16HMM_TF/100223/{mutant}/')



#Example for overexp for which things to put in as args
# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16mut44_092623', wt_fac =2, mut_fac = 0, 
#                                amp = 0.5, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111623/100WT/',
#                                fnpre = '100WT_w2m0_111623', wtorhet = 'WT')




##Scan na12na16 for all mutants in jupytermutant list.
# Run all synth muts at multiple points along neuron 012324
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
# #2
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
# # #3
# # sim_config_basaldend = {
# #                 'section' : 'dend',
# #                 'segment' : 0.5,
# #                 'section_num': 70,
# #                 #'currents' : ['ina','ica','ik'],
# #                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
# #                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
# #                 #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
# #                 'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2'], #dend (no Ih, no ik_SKv3_1)
# #                 'current_names' : ['Ih','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
# #                 #'ionic_concentrations' :["cai", "ki", "nai"]
# #                 'ionic_concentrations' :["ki", "nai"]
# #                 }
# #4
# sim_config_nexus = {
#                 'section' : 'apic',
#                 'segment' : 0,
#                 'section_num': 77,
#                 #'currents' : ['ina','ica','ik'],
#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
#                 'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
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
#                 #'currents' : ['ina','ica','ik'],
#                 #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], #Somatic
#                 'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ik_SK_E2','ik_SKv3_1'], #AIS (no Ih)
#                 #'currents'  : ['ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 #'currents'  : ['ihcn_Ih','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'],
#                 #'ionic_concentrations' :["cai", "ki", "nai"]
#                 'ionic_concentrations' :["ki", "nai"]
#                 }


# root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/AdilVariants012524/'

# if not os.path.exists(root_path_out):
#         os.mkdir(root_path_out)


# #Make WT and save data for comparison later
# sim = tf.Na12Model_TF(nav12=2.25,nav16=2,na12name = 'na12_HMM_TF100923',mut_name = 'na12_HMM_TF100923',
#                 params_folder = './params/na12HMM_allsynthmuts_HOFs/',
#                 plots_folder = f'{root_path_out}_hmmWT', pfx=f'WT_')

# #soma
# wt_Vm1,wt_I1,wt_t1,wt_stim1 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
# features_df = ef.get_features(sim=sim,mutTXT='WT_soma', mut_name = 'na12_HMM_TF100923')

# #ais
# # wt_Vm2,wt_I2,wt_t2,wt_stim2 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_ais)
# # features_df = ef.get_features(sim=sim,mutTXT='WT_ais', mut_name = 'na12_HMM_TF100923')

# # # wt_Vm3,wt_I3,wt_t3,wt_stim3 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_basaldend)
# # # features_df = ef.get_features(sim=sim,mutTXT='WT_basaldend', mut_name = 'na12_HMM_TF100923')

# # wt_Vm4,wt_I4,wt_t4,wt_stim4 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_nexus)
# # features_df = ef.get_features(sim=sim,mutTXT='WT_nexus', mut_name = 'na12_HMM_TF100923')

# # wt_Vm5,wt_I5,wt_t5,wt_stim5 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_apicaldend)
# # features_df = ef.get_features(sim=sim,mutTXT='WT_apicaldend', mut_name = 'na12_HMM_TF100923')

# ###  Make directories with names from list in txt file (mutant_names.txt)
# file = open('/global/homes/t/tfenton/Neuron_general-2/JUPYTERmutant_list.txt','r')
# Lines = file.readlines()
# for line in Lines:
#         print (line)
#         mutTXT = line.strip()
#         path = os.path.join(root_path_out,mutTXT)
#         # if not os.path.exists(path):
#         #         os.mkdir(path)

#         print (mutTXT)
#         print(line)



#         sim = tf.Na12Model_TF(nav12=2.25,nav16=2,na12name = 'na12_HMM_TF100923',mut_name = mutTXT+'_010524HOF',
#                         params_folder = './params/Manuscript_adilvariants/',
#                         plots_folder = f'{root_path_out}/{mutTXT}_ais/', pfx=f'{mutTXT}')


#         #make spiking and dvdt plots
#         #sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm,wt_t=wt_t,vs_amp=[0.5], fnpre=f'{mutTXT}_Na16-{i16}')
        
#         #soma
#         sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'{mutTXT}_soma')
#         features_df = ef.get_features(sim=sim,mutTXT=f'{root_path_out}/{mutTXT}_soma', mut_name = mutTXT+'_010524HOF')
        
#         #ais
#         # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm2,wt_t=wt_t2,sim_config=sim_config_ais,vs_amp=[0.5], fnpre=f'{mutTXT}_ais')
#         # features_df = ef.get_features(sim=sim,mutTXT=f'{mutTXT}_ais', mut_name = mutTXT+'_121123')

#         # # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm3,wt_t=wt_t3,sim_config=sim_config_basaldend,vs_amp=[0.5], fnpre=f'{mutTXT}_basaldend')
#         # # features_df = ef.get_features(sim=sim,mutTXT=f'{mutTXT}_basaldend', mut_name = mutTXT+'_121123')

#         # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm4,wt_t=wt_t4,sim_config=sim_config_nexus,vs_amp=[0.5], fnpre=f'{mutTXT}_nexus')
#         # features_df = ef.get_features(sim=sim,mutTXT=f'{mutTXT}_nexus', mut_name = mutTXT+'_121123')

#         # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm5,wt_t=wt_t5,sim_config=sim_config_apicaldend,vs_amp=[0.5], fnpre=f'{mutTXT}_apicaldend')
#         # features_df = ef.get_features(sim=sim,mutTXT=f'{mutTXT}_apicaldend', mut_name = mutTXT+'_121123')

#         #make currentscape plots
#         sim.make_currentscape_plot(amp=0.5, time1=25,time2=60,stim_start=30, sweep_len=75)
#         sim.make_currentscape_plot(amp=0.5, time1=0,time2=100,stim_start=30, sweep_len=100)


#         #Electrophys Feature Extraction Library efel
#         # features_df = ef.get_features(sim=sim, mut_name = mutTXT+'_121123')
# # features_df.to_csv(f'{root_path_out}/{mutTXT}/{mutTXT}_features.csv', index=False) ##save efeatures to csv

#################################################################################






#################################################################################
#################################################################################
########## Getting WTs for paper figures HH WT and HMM WT


        #section[section_num](segment)
        #Section: soma, section_num: 0, segment:0.5 == Middle of Soma
        #Section: axon, section_num:0, segment:0 == AIS
        #Section: dend, section_num: 70, segment: 0.5 == Basal dendrite mid-shaft ***should check this in gui
        #Section: apic, section_num:77, segment:0       77(0) or 66(1)  == Apical Nexus
        #Section: apic, section_num:90, segment:0.5   == Most distal apical dendrite
# sim_config = {
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


# root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/SynthMuts/'


# if not os.path.exists(root_path_out):
#     os.makedirs(root_path_out)


# #Make HH WT and save data for comparison later
# #Make HMM WT for synth muts comparison
# sim = tf.Na12Model_TF(nav12=2.25,nav16=2,na12name = 'na12_HMM_TF100923',mut_name = 'na12_HMM_TF100923',
#                 params_folder = './params/Manuscript_HH_HMM_WTs/',
#                 plots_folder = f'{root_path_out}', pfx=f'HH_Soma')

# wt_Vm,wt_I,wt_t,wt_stim = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config=sim_config_soma)

# #make currentscape plots HH
# # sim.make_currentscape_plot(amp=0.5, time1=25,time2=60,stim_start=30, sweep_len=75,sim_config=sim_config)
# # sim.make_currentscape_plot(amp=0.5, time1=0,time2=100,stim_start=30, sweep_len=100,sim_config=sim_config)

# #Electrophys Feature Extraction Library efel -- HH

# features_df = ef.get_features(sim=sim, mut_name = 'na12_orig1')

# # with open (f'{root_path_out}HH_soma_features.csv','a') as f1:
# #     features_df.to_csv(f1,index=False) ##save efeatures to csv

# #features_df.to_csv(f'{root_path_out}/HH_soma_features.csv') ##save efeatures to csv



# # Make HMM WT -- will be in red as 'mutant'
# # Make HMM synth muts -- mut will be in red
# sim = tf.Na12Model_TF(nav12=2.25,nav16=2,na12name = 'na12_HMM_TF100923',mut_name = 'na12_HMM_TF100923',
#                 params_folder = './params/Manuscript_HH_HMM_WTs/',
#                 plots_folder = f'{root_path_out}', pfx=f'HMM_soma')


# #make spiking and dvdt plots
# # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm,wt_t=wt_t,sim_config=sim_config,vs_amp=[0.5], fnpre=f'HH_blk_basaldend_')


# #make currentscape plots HMM
# # sim.make_currentscape_plot(amp=0.5, time1=25,time2=60,stim_start=30, sweep_len=75,sim_config=sim_config)
# # sim.make_currentscape_plot(amp=0.5, time1=0,time2=100,stim_start=30, sweep_len=100,sim_config=sim_config)


# #Electrophys Feature Extraction Library efel --HMM
# features_df2 = ef.get_features(sim=sim, mut_name = 'na12_HMM_TF100923')
# print(features_df2)
# # with open (f'{root_path_out}HH_soma_features.csv','a') as f2:
# #     features_df.to_csv(f2,index=False) ##save efeatures to csv
# #features_df2.to_csv(f'{root_path_out}/HMM_soma_features.csv') ##save efeatures to csv














##Scan ais_nav16 to reduce from ~7 to range(.01,1) by .05
##020224 Scan other params (K, na12, soma_na12)
#################################################################################


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


# root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/Restart030824/6-HMM_focusonTTP_042624/10-12HMMmuts_fitto_1012TTP8_050824'
root_path_out = './Plots/12HMM16HMM/11-12hmmOptScan_071424'

if not os.path.exists(root_path_out):
        os.makedirs(root_path_out)
        # os.mkdir(root_path_out)


vals =[4,6,8]
vals2 = [2]

# for i12 in np.arange(2,3,1):     
#       for i16 in np.arange(7,8,1):
for i12 in vals:
        for i16 in vals2:
                ##Adding below function to loop through different na16.mod params        
                # filename = "/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TF100923-2.txt" ##TF031524 for changing 8st na12
                filename12 = './params/na12_HMM_TEMP_PARAMS.txt'
                filename16 = './params/na16_HMM_TEMP_PARAMS.txt'

                
                               
                ##TF052024 mut10_12_TTP8 (from 050624) better WT (fit to mut10_9_TTP8)
                changesna12={"a1_0": 62.774771313021546, 
                        "a1_1": 0.6854152336583206,
                        "b1_0": 3.2117067311143277,
                        "b1_1": 0.1432460480232296, 
                        "a2_0": 2468.966900014909,
                        "a2_1": 0.0834387238328, 
                        "b2_0": 490.16060600231606,
                        "b2_1": 2.969500725999265,
                        "a3_0": 190.5883640336242,
                        "a3_1": 0.003108395956123883,
                        "b3_0": 7689.251014289831, 
                        "b3_1": 0.04054164070835632,
                        "bh_0": 4.063594186259147,
                        "bh_1": 2.115884898210715, 
                        "bh_2": 0.1433653421971472,
                        "ah_0": 1.3563238605774417,
                        "ah_1": 6568.351916792737, 
                        "ah_2": 0.011127551783912584,
                        "vShift": -18.276678986708095, 
                        "vShift_inact": 16.74204011921361, 
                        "maxrate": 6.170113221706686}
                
                ##mut10_4, testing for altered tau WT 061124                
                # changesna12={"a1_0": 30.990568607464937, "a1_1": 0.727207131085451, "b1_0": 2.4177659248112304, "b1_1": 0.001361137402837942, "a2_0": 7764.878961142766, "a2_1": 0.033710133967452593, "b2_0": 354.5075793923026, "b2_1": 4.0585190172293055, "a3_0": 124.65125337416927, "a3_1": 0.002466385979914096, "b3_0": 5691.006145002193, "b3_1": 0.0062791739575876, "bh_0": 0.7148812999656258, "bh_1": 1.0205850850329137, "bh_2": 0.1491648507752708, "ah_0": 11.231511989775173, "ah_1": 29046.460566891234, "ah_2": 0.008490668279800669, "vShift": -19.00612418597558, "vShift_inact": 8.677200690072695, "maxrate": 5.262143195447436}
                
                ##TF052824 16HMM WT from Moran na16mut44_092623
                changesna16={"a1_0": 9.943980540891205, 
                        "a1_1": 0.09023475298110195, 
                        "b1_0": 4.809469162333778, 
                        "b1_1": 0.00021253413520036122, 
                        "a2_0": 3699.864927408996, 
                        "a2_1": 0.014825840578195144, 
                        "b2_0": 32.94719611096497, 
                        "b2_1": 0.043572007893336887,
                        "a3_0": 428.4532637061227, 
                        "a3_1": 0.1993700855837062, 
                        "b3_0": 45.50266263937303, 
                        "b3_1": 0.004565244221972131,
                        "bh_0": 6.623769188984069, 
                        "bh_1": 7.348567323368201, 
                        "bh_2": 0.13171436477580875, 
                        "ah_0": 5.722632232902148, 
                        "ah_1": 1820.0789387156779, 
                        "ah_2": 0.013864995417150049, 
                        "vShift": -9.719627438867658, 
                        "vShift_inact": 3.2360259605403203, 
                        "maxrate": 54.784511287581864}
                
                changesna16a={"a1_0": 8.0578874919151, "a1_1": 0.0362460004441742, "b1_0": 0.2975424360004787, "b1_1": 0.019626504231602726, "a2_0": 7541.367908495317, "a2_1": 0.008115928598620786, "b2_0": 37.78264401293287, "b2_1": 13.197541674645006, "a3_0": 2661.4548837273387, "a3_1": 0.28322186815760786, "b3_0": 41.45025415671522, "b3_1": 0.005946538949708524, "bh_0": 4.957064052666118, "bh_1": 14.94315170855162, "bh_2": 0.10627633864486724, "ah_0": 0.3348261287268917, "ah_1": 1847.8521286814391, "ah_2": 0.04174076351521052, "vShift": -9.569584432015834, "vShift_inact": 2.352045239220809, "maxrate": 44.84946684890218}
                changesna16b = {"a1_0": 9.090328600911736, "a1_1": 0.011144987169071197, "b1_0": 9.255699008849243, "b1_1": 0.0016137523402601096, "a2_0": 10932.78658636546, "a2_1": 0.29192427179674435, "b2_0": 15.767473317100103, "b2_1": 25.93317454739589, "a3_0": 390.30935790084703, "a3_1": 0.025356749923664747, "b3_0": 46.64622013957142, "b3_1": 0.018170036985660443, "bh_0": 1.6059822779031636, "bh_1": 3.7393826933625283, "bh_2": 0.1426405180186169, "ah_0": 2.2070454502199075, "ah_1": 38282.91375852737, "ah_2": 0.08991604167580454, "vShift": -8.808787096096369, "vShift_inact": -3.981655239131775, "maxrate": 36.56718201895245}

                ##Uncomment if want to update params file to update mod file!!!
                nf.modify_dict_file(filename12, changesna12)
                # nf.modify_dict_file(filename16, changesna16)
                nf.modify_dict_file(filename16, changesna16b)
                
                ##TF061324 decent 1216HMM WT best so far
                # simwt = tf.Na12Model_TF(ais_nav12_fac=15,ais_nav16_fac=15,nav12=2.75,nav16=2.75, somaK=1, KP=70, KT=1, #ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=50, KT=1
                #                 ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                #                 na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                #                 na16name = 'na16mut44_092623',na16mut_name = 'na16mut44_092623',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/1-WT', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                


                ##TF071124
                simwt = tf.Na12Model_TF(ais_nav12_fac=24,ais_nav16_fac=3,nav12=6,nav16=4, somaK=1, KP=100, KT=1, ##070324 nav12=6, nav16=4 ##062424 ais_nav12_fac=10,ais_nav16_fac=10,nav12=4,nav16=2.5 #ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=50, KT=1
                                ais_ca = 10,ais_Kca = 10, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/16-caHVA-0.1_50HET', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
                wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                
                
                # fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                # ap_t, vm_t = simwt.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
                # # nf.plot_8states(csv_name="/global/homes/t/tfenton/Neuron_general-2/Plots/Channel_state_plots/na12_channel_states.csv", outfile_sfx="na12_1216-00_062824",ap_t=ap_t, vm_t=vm_t )
                # # nf.plot_8states(csv_name="/global/homes/t/tfenton/Neuron_general-2/Plots/Channel_state_plots/na16_channel_states.csv", outfile_sfx="na16_1216-00_062824",ap_t=ap_t, vm_t=vm_t )
                # plot_dvdt_from_volts(simwt.volt_soma, simwt.dt, axs[1],clr='cadetblue')
                # fig_volts.savefig(f'{simwt.plot_folder}/16-caHVA-0.1_50HET.pdf')
                # simwt.make_currentscape_plot(amp=0.5, time1=100,time2=400,stim_start=100, sweep_len=800)

                # simwt.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)


                
                changesna16a={"mut10_4": {"a1_0": 8.0578874919151, "a1_1": 0.0362460004441742, "b1_0": 0.2975424360004787, "b1_1": 0.019626504231602726, "a2_0": 7541.367908495317, "a2_1": 0.008115928598620786, "b2_0": 37.78264401293287, "b2_1": 13.197541674645006, "a3_0": 2661.4548837273387, "a3_1": 0.28322186815760786, "b3_0": 41.45025415671522, "b3_1": 0.005946538949708524, "bh_0": 4.957064052666118, "bh_1": 14.94315170855162, "bh_2": 0.10627633864486724, "ah_0": 0.3348261287268917, "ah_1": 1847.8521286814391, "ah_2": 0.04174076351521052, "vShift": -9.569584432015834, "vShift_inact": 2.352045239220809, "maxrate": 44.84946684890218}}

                #TF062124 runs changing objectives 2,4, and 10 in na16hmm
                changesna16a={#"mut24_3":{"a1_0": 9.97325723123336, "a1_1": 0.04493007966899823, "b1_0": 18.906410431058035, "b1_1": 0.013032651106964149, "a2_0": 13392.43771410394, "a2_1": 0.010567185317746603, "b2_0": 47.518234251552585, "b2_1": 5.618088304677881, "a3_0": 2305.5646542684117, "a3_1": 0.0189404561624361, "b3_0": 36.53340836886169, "b3_1": 0.012011682818820146, "bh_0": 11.5065870954496, "bh_1": 2.8427183738413193, "bh_2": 0.08252387220268713, "ah_0": 0.17867628374563282, "ah_1": 183826.24796890566, "ah_2": 0.17821061809968056, "vShift": -3.3990943655193693, "vShift_inact": -2.3484619351039138, "maxrate": 23888.72364587752},
                        #"mut2410_2":{"a1_0": 10.0, "a1_1": 0.0012063013149955053, "b1_0": 14.55146153023609, "b1_1": 0.059786088424921516, "a2_0": 5490.070311976771, "a2_1": 0.0996861941041664, "b2_0": 50.0, "b2_1": 0.3231235157083805, "a3_0": 198.54687300633066, "a3_1": 0.04206823146439518, "b3_0": 49.47644229146293, "b3_1": 0.1565371735857367, "bh_0": 8.011805611317342, "bh_1": 14.929874425885203, "bh_2": 0.0549541211025924, "ah_0": 1.09714159118842, "ah_1": 66682.01097053559, "ah_2": 0.028652975601013472, "vShift": -5.151171107498385, "vShift_inact": 14.469170935119013, "maxrate": 5.871373675016002},
                        "mut2410_5":{"a1_0": 9.090328600911736, "a1_1": 0.011144987169071197, "b1_0": 9.255699008849243, "b1_1": 0.0016137523402601096, "a2_0": 10932.78658636546, "a2_1": 0.29192427179674435, "b2_0": 15.767473317100103, "b2_1": 25.93317454739589, "a3_0": 390.30935790084703, "a3_1": 0.025356749923664747, "b3_0": 46.64622013957142, "b3_1": 0.018170036985660443, "bh_0": 1.6059822779031636, "bh_1": 3.7393826933625283, "bh_2": 0.1426405180186169, "ah_0": 2.2070454502199075, "ah_1": 38282.91375852737, "ah_2": 0.08991604167580454, "vShift": -8.808787096096369, "vShift_inact": -3.981655239131775, "maxrate": 36.56718201895245}}
                
                changesna16b={"mut2410_5":{"a1_0": 9.090328600911736, "a1_1": 0.011144987169071197, "b1_0": 9.255699008849243, "b1_1": 0.0016137523402601096, "a2_0": 10932.78658636546, "a2_1": 0.29192427179674435, "b2_0": 15.767473317100103, "b2_1": 25.93317454739589, "a3_0": 390.30935790084703, "a3_1": 0.025356749923664747, "b3_0": 46.64622013957142, "b3_1": 0.018170036985660443, "bh_0": 1.6059822779031636, "bh_1": 3.7393826933625283, "bh_2": 0.1426405180186169, "ah_0": 2.2070454502199075, "ah_1": 38282.91375852737, "ah_2": 0.08991604167580454, "vShift": -8.808787096096369, "vShift_inact": -3.981655239131775, "maxrate": 36.56718201895245}}

                
                ##TF071124 Testing different na16hmm and na12hmm new fits
                ###################### 16HMM ######################
                changesna16_071124 ={"mut2410_10_TTP1":{"a1_0": 9.742196766662957, "a1_1": 0.10024433386068651, "b1_0": 23.88620531728156, "b1_1": 0.0509919203063276, "a2_0": 8567.884901518655, "a2_1": 0.2141642588265052, "b2_0": 49.43499256203817, "b2_1": 8.791800882710179, "a3_0": 130.55043097455115, "a3_1": 0.05341559051125212, "b3_0": 45.988293058104375, "b3_1": 0.041368234531536846, "bh_0": 1.7124757382524196, "bh_1": 2.0111045757094272, "bh_2": 0.12487117791440071, "ah_0": 0.12511625514487623, "ah_1": 358937.71241625724, "ah_2": 0.13691187988442272, "vShift": -9.371919214156653, "vShift_inact": -8.466310459891169, "maxrate": 3.287576013785187},
                        # "mut2410_11_TTP1":{"a1_0": 9.997971857215473, "a1_1": 0.013843345720747482, "b1_0": 31.667130909892823, "b1_1": 0.06299212327360912, "a2_0": 11819.85197427201, "a2_1": 0.02826860811859131, "b2_0": NaN, "b2_1": 0.006626235385942536, "a3_0": 138.73829102589056, "a3_1": 0.10023016334797899, "b3_0": 49.999392808425824, "b3_1": 0.6040856692420429, "bh_0": 32.78032583395509, "bh_1": 11.364567599708545, "bh_2": 0.06433520034178512, "ah_0": 4.069586289468035, "ah_1": 782263.3792876563, "ah_2": 0.08706670005790429, "vShift": NaN, "vShift_inact": -0.2959693635469607, "maxrate": 3.1772816229850367},
                        # "mut2410_12_TTP1":{"a1_0": 9.389504923103386, "a1_1": 0.0036414087479368163, "b1_0": 33.1348438930777, "b1_1": 0.037728911618474026, "a2_0": 1663.1438640777287, "a2_1": 0.05135036158444409, "b2_0": NaN, "b2_1": 0.0974392876486494, "a3_0": 377.3382476971053, "a3_1": 0.130499742891303, "b3_0": NaN, "b3_1": 0.03445114112211063, "bh_0": 2.1376650143277063, "bh_1": 0.05989926625149712, "bh_2": 0.11454161403348508, "ah_0": 1.227155215208738, "ah_1": 237696.66734486155, "ah_2": 0.08710916930492157, "vShift": -9.622853793498955, "vShift_inact": 2.6891757369426044, "maxrate": 3218.7551176962174},
                        "mut2410_13_TTP1":{"a1_0": 7.285744152118881, "a1_1": 0.08152685120572217, "b1_0": 0.1332984704579383, "b1_1": 0.045334516352472536, "a2_0": 8431.511036053256, "a2_1": 0.2004695510223511, "b2_0": 45.694393770785396, "b2_1": 4.470280778784577, "a3_0": 1567.7802919217609, "a3_1": 0.15430220692205762, "b3_0": 34.37277743053083, "b3_1": 0.008406996053669194, "bh_0": 4.180223041930371, "bh_1": 6.622702072006549, "bh_2": 0.07169222684322177, "ah_0": 0.6266673057473958, "ah_1": 86420.85683719994, "ah_2": 0.10029469377934437, "vShift": -9.655671472971061, "vShift_inact": 1.4755010372501618, "maxrate": 4.941617071284247},
                        "mut2410_14_TTP1":{"a1_0": 9.962400477950574, "a1_1": 0.026258320239377297, "b1_0": 5.341652079659072, "b1_1": 0.05338572393968217, "a2_0": 7474.761830881351, "a2_1": 0.18826043882937646, "b2_0": 40.337183138108045, "b2_1": 14.760887753158949, "a3_0": 149.77165088287165, "a3_1": 0.047092757305149974, "b3_0": 35.19013573528861, "b3_1": 0.030509433980001277, "bh_0": 9.57421303631399, "bh_1": 0.1416528759577141, "bh_2": 0.09397426244648849, "ah_0": 2.480028784503978, "ah_1": 409.5518239238188, "ah_2": 0.020008969959328066, "vShift": -8.406673671989768, "vShift_inact": 14.288864931406994, "maxrate": 19.321422532135514},
                        # "mut2410_15_TTP1":{"a1_0": 9.696566871285457, "a1_1": 0.004881896113769785, "b1_0": 23.567801289821663, "b1_1": 0.048790092751401185, "a2_0": 10848.033265447018, "a2_1": 0.16689173532304263, "b2_0": 41.288884770063774, "b2_1": 17.980489787882785, "a3_0": 624.6979355861395, "a3_1": 0.04200508672215998, "b3_0": NaN, "b3_1": 0.0637630980011741, "bh_0": 18.983685025867963, "bh_1": 0.28413741089894096, "bh_2": 0.0913668155514929, "ah_0": 5.172228950343842, "ah_1": 258802.7564869086, "ah_2": 0.06644207179245465, "vShift": NaN, "vShift_inact": 10.262144831209518, "maxrate": 8.16200517369412},
                        "mut2410_16_TTP1":{"a1_0": 9.09263877478807, "a1_1": 0.010251121049808055, "b1_0": 0.1759797522433597, "b1_1": 0.04454743359609606, "a2_0": 9280.20681320547, "a2_1": 0.23466761376369177, "b2_0": 49.766524912549855, "b2_1": 20.73134958819324, "a3_0": 14.490757639578614, "a3_1": 0.037663625733858785, "b3_0": 50.0, "b3_1": 0.5040421406577031, "bh_0": 41.65178351929038, "bh_1": 16.19549879062815, "bh_2": 0.09897023892521196, "ah_0": 0.7000125463184027, "ah_1": 212077.4407000157, "ah_2": 0.07739378277749637, "vShift": -5.800124401680381, "vShift_inact": 2.6215586898880083, "maxrate": 4.969515748953646},
                        # "mut2410_10_TTP2":{"a1_0": NaN, "a1_1": 0.05435014793357833, "b1_0": 27.85311540755694, "b1_1": 0.06782126483693864, "a2_0": 15494.267753784907, "a2_1": 0.26809250754452874, "b2_0": 50.0, "b2_1": 0.13999217995849744, "a3_0": 2816.2193225296214, "a3_1": 0.029384767388326804, "b3_0": 49.79935783701755, "b3_1": 0.12453742558340178, "bh_0": 14.300596418498678, "bh_1": 7.794215476062805, "bh_2": 0.11808496902465143, "ah_0": 1.4482917427017246, "ah_1": 305496.36709574034, "ah_2": 0.09642541627114362, "vShift": -4.645498637834965, "vShift_inact": -8.088406292512207, "maxrate": 3.95709158874012},
                        "mut2410_11_TTP2":{"a1_0": 8.566455407752812, "a1_1": 0.00176386976781151, "b1_0": 25.85318246160774, "b1_1": 0.08011049139841256, "a2_0": 11115.675459843898, "a2_1": 0.19399865582631803, "b2_0": 49.171757889004226, "b2_1": 6.968926493577525, "a3_0": 141.1726556558072, "a3_1": 0.009966668472573399, "b3_0": 41.83382890694062, "b3_1": 1.9528382248297327, "bh_0": 6.84704593202799, "bh_1": 0.9491294603253948, "bh_2": 0.04835551921851143, "ah_0": 0.2301153869945332, "ah_1": 41705.7996947748, "ah_2": 0.09303291718902008, "vShift": 2.1476179262905717, "vShift_inact": 23.586360780680298, "maxrate": 3.7436910920470243},
                        "mut2410_12_TTP2":{"a1_0": 8.936838640453889, "a1_1": 0.033831797979228924, "b1_0": 2.7885210232834194, "b1_1": 0.04409249897454566, "a2_0": 1653.7014632129544, "a2_1": 0.18168023113549023, "b2_0": 46.809999361487364, "b2_1": 23.16669049534004, "a3_0": 151.35881951059343, "a3_1": 0.01949602138864572, "b3_0": 36.81723159218738, "b3_1": 0.6888927818698486, "bh_0": 20.863657969521814, "bh_1": 4.644833270073347, "bh_2": 0.09696920023289285, "ah_0": 0.3610609816613818, "ah_1": 156665.51599077554, "ah_2": 0.09471433570855554, "vShift": -6.011210595898984, "vShift_inact": -2.5590534311180217, "maxrate": 7.547686008129865}}
                        # "mut2410_13_TTP2":{"a1_0": 6.697422290603381, "a1_1": 0.011254337443037277, "b1_0": 7.576851880029415, "b1_1": 0.029215085622426144, "a2_0": 16993.04891800459, "a2_1": 0.347607352534853, "b2_0": NaN, "b2_1": 2.70312179500962, "a3_0": 514.7177082456866, "a3_1": 0.036034544086339104, "b3_0": NaN, "b3_1": 0.0013217700622544862, "bh_0": 6.190662416976455, "bh_1": 2.631946367111532, "bh_2": 0.13371051595783812, "ah_0": NaN, "ah_1": 189199.88152927926, "ah_2": 0.03859748181819894, "vShift": -9.366094358861446, "vShift_inact": -8.432622496005813, "maxrate": 2.9733373641466225}}
                changesna16_071124best = {"mut2410_13_TTP1":{"a1_0": 7.285744152118881, "a1_1": 0.08152685120572217, "b1_0": 0.1332984704579383, "b1_1": 0.045334516352472536, "a2_0": 8431.511036053256, "a2_1": 0.2004695510223511, "b2_0": 45.694393770785396, "b2_1": 4.470280778784577, "a3_0": 1567.7802919217609, "a3_1": 0.15430220692205762, "b3_0": 34.37277743053083, "b3_1": 0.008406996053669194, "bh_0": 4.180223041930371, "bh_1": 6.622702072006549, "bh_2": 0.07169222684322177, "ah_0": 0.6266673057473958, "ah_1": 86420.85683719994, "ah_2": 0.10029469377934437, "vShift": -9.655671472971061, "vShift_inact": 1.4755010372501618, "maxrate": 4.941617071284247}}
                ###################### 16HMM ######################



                
                ###################### 12HMM ######################
                changesna12_071124 ={"mut35_1":{"a1_0": 26.661136396347647, "a1_1": 0.4397818616258945, "b1_0": 5.140546977803373, "b1_1": 0.0023786794800046496, "a2_0": 12201.005250820219, "a2_1": 0.11225805982856737, "b2_0": 795.6214721562169, "b2_1": 2.705337837041022, "a3_0": 1.0603212942807403, "a3_1": 0.017801745347518175, "b3_0": 4238.068061080703, "b3_1": 0.04663042389645128, "bh_0": 5.375979908468794, "bh_1": 7.4245935612239755, "bh_2": 0.13693156222539066, "ah_0": 0.38481576084217384, "ah_1": 81601.43307745905, "ah_2": 0.0515675108299225, "vShift": -20.9255657024864, "vShift_inact": 16.05619235556432, "maxrate": 9.287775125513424},
                        "mut35_3":{"a1_0": 86.17634499794501, "a1_1": 0.5105933633695633, "b1_0": 0.46469773746998366, "b1_1": 0.011836807583451086, "a2_0": 8237.491561711813, "a2_1": 0.007276256307606831, "b2_0": 589.3448849203317, "b2_1": 2.1518744598898936, "a3_0": 121.46579920692959, "a3_1": 0.014875146391778227, "b3_0": 6751.495761184102, "b3_1": 0.049790677051081644, "bh_0": 1.9375516630163112, "bh_1": 9.64219151756209, "bh_2": 0.11380326226424994, "ah_0": 12.051666573376338, "ah_1": 11497.735358174352, "ah_2": 0.0008694618266809756, "vShift": -19.76353307872219, "vShift_inact": 9.256747306925453, "maxrate": 5133.267048270342},
                        "mut35_1_TTP1":{"a1_0": 348.791542516338, "a1_1": 1.4519803869729961, "b1_0": 2.377490652073381, "b1_1": 0.031145794769299587, "a2_0": 6387.165893866789, "a2_1": 0.08812366089142246, "b2_0": 457.6023064966458, "b2_1": 1.9622879899017416, "a3_0": 291.0873606087262, "a3_1": 0.035455049938548255, "b3_0": 6086.195583510338, "b3_1": 0.04584674766638497, "bh_0": 1.0867691591754813, "bh_1": 6.941772181771312, "bh_2": 0.20529363303574705, "ah_0": 0.43837758575994057, "ah_1": 17213.373141546806, "ah_2": 0.03498442786390603, "vShift": -28.364673291190734, "vShift_inact": 0.06485333458063236, "maxrate": 1448.075816345098},
                        "mut35_2_TTP1":{"a1_0": 56.384880063722775, "a1_1": 1.6845039453978703, "b1_0": 1.6467552793942548, "b1_1": 0.0349906708327795, "a2_0": 13499.506370380372, "a2_1": 0.332865824291677, "b2_0": 352.27764800103563, "b2_1": 1.8110979549707555, "a3_0": 235.5662937426644, "a3_1": 0.0122185240376384, "b3_0": 3556.0138487858694, "b3_1": 0.05475950459159293, "bh_0": 2.9288200810712297, "bh_1": 11.638337549310396, "bh_2": 0.14881968061721987, "ah_0": 0.7668391200465918, "ah_1": 10335.684020338136, "ah_2": 0.028295988717464637, "vShift": -26.05004875897014, "vShift_inact": 9.735318222604503, "maxrate": 1845.258154113959}}
                changesna12_071124best = {"mut35_3":{"a1_0": 86.17634499794501, "a1_1": 0.5105933633695633, "b1_0": 0.46469773746998366, "b1_1": 0.011836807583451086, "a2_0": 8237.491561711813, "a2_1": 0.007276256307606831, "b2_0": 589.3448849203317, "b2_1": 2.1518744598898936, "a3_0": 121.46579920692959, "a3_1": 0.014875146391778227, "b3_0": 6751.495761184102, "b3_1": 0.049790677051081644, "bh_0": 1.9375516630163112, "bh_1": 9.64219151756209, "bh_2": 0.11380326226424994, "ah_0": 12.051666573376338, "ah_1": 11497.735358174352, "ah_2": 0.0008694618266809756, "vShift": -19.76353307872219, "vShift_inact": 9.256747306925453, "maxrate": 5133.267048270342}}

                ##071424 midopt
                changesna12_071424mid = {#"2-mut3_8_TTP2":{"a1_0": 258.5559655039012, "a1_1": 1.8330589346454356, "b1_0": 1.5087844268592576, "b1_1": 0.14870424805317267, "a2_0": 13093.550343518222, "a2_1": 0.21641045015611357, "b2_0": 383.9683408743241, "b2_1": 1.3894359070518334, "a3_0": 302.0593381026973, "a3_1": 0.013228103456894989, "b3_0": 4750.537162534246, "b3_1": 0.05218833017046101, "bh_0": 2.8217316979366593, "bh_1": 21.77565271141875, "bh_2": 0.13464104678643227, "ah_0": 0.3134814383833766, "ah_1": 252699.64376715725, "ah_2": 0.05218429368523682, "vShift": -26.186685988529927, "vShift_inact": 8.76712222865394, "maxrate": 2425.781937166357},
                        #"2-mut3_8_TTP3":{"a1_0": 43.006788240340704, "a1_1": 0.35621825050576894, "b1_0": 1.1306763804129167, "b1_1": 0.004790328723724882, "a2_0": 7517.279142835591, "a2_1": 0.15639403829324422, "b2_0": 492.57584465117407, "b2_1": 0.46234124832959295, "a3_0": 156.17563910453885, "a3_1": 3.790801341570105e-05, "b3_0": 5376.232680487549, "b3_1": 0.07140872406233476, "bh_0": 4.007350449938738, "bh_1": 5.888423838160996, "bh_2": 0.13216441003338797, "ah_0": 10.880485240737304, "ah_1": 3978.614774723057, "ah_2": 0.0013381031263370452, "vShift": -16.06943393975376, "vShift_inact": 3.3663573250511005, "maxrate": 78.76867353966634},
                        #"2-mut3_8_TTP4":{"a1_0": 1.0827197320454074, "a1_1": 1.9725602840912588, "b1_0": 5.147350064242216, "b1_1": 0.015416382982224298, "a2_0": 7585.771188110223, "a2_1": 0.1653507988884675, "b2_0": 345.6764832141528, "b2_1": 1.6547961735349381, "a3_0": 199.13317487417015, "a3_1": 0.017124252424555793, "b3_0": 2916.369695997244, "b3_1": 0.02874397578268614, "bh_0": 2.9673278180753253, "bh_1": 6.709204786895002, "bh_2": 0.12656256078250266, "ah_0": 1.1073303804313759, "ah_1": 21061.5886186682, "ah_2": 0.012185395220615174, "vShift": -25.97454482195446, "vShift_inact": 20.3522684039795, "maxrate": 3193.472775380896},
                        "2-mut35_4_TTP3":{"a1_0": 9.16784152366466, "a1_1": 0.7498178403322555, "b1_0": 0.9250870194676788, "b1_1": 0.04570797312462545, "a2_0": 7704.249958014978, "a2_1": 0.07214921966679647, "b2_0": 452.3191520712655, "b2_1": 0.12255643006613637, "a3_0": 232.5675642385227, "a3_1": 0.0009196164331762738, "b3_0": 2700.131799836734, "b3_1": 0.04647017715031404, "bh_0": 1.6360257082819747, "bh_1": 8.288348422797782, "bh_2": 0.15334359789813812, "ah_0": 8.163461917843849, "ah_1": 128110.04424496027, "ah_2": 0.008007538690100603, "vShift": -23.344349669193836, "vShift_inact": 3.3114728957733703, "maxrate": 2027.3605771235598},
                        #"2-mut35_5_TTP3":{"a1_0": 84.83944514131778, "a1_1": 1.330686998660016, "b1_0": 2.571711482872911, "b1_1": 0.09648417712733517, "a2_0": 3625.734478449313, "a2_1": 0.12135771988381855, "b2_0": 429.9829222118584, "b2_1": 0.011367191048575087, "a3_0": 275.0321342323549, "a3_1": 0.08603481781998171, "b3_0": 4226.495554111414, "b3_1": 0.01914082980332335, "bh_0": 2.670450293345347, "bh_1": 5.539178043351134, "bh_2": 0.15206827761174918, "ah_0": 0.19771940570291768, "ah_1": 21056.360527225275, "ah_2": 0.0352567587629395, "vShift": -22.80351068749592, "vShift_inact": 10.61671991177511, "maxrate": 549.0157352267477},
                        #"2-mut2345_1_TTP3":{"a1_0": 82.50802007186184, "a1_1": 0.32985432817041405, "b1_0": 2.74949832298816, "b1_1": 0.052470072459455994, "a2_0": 10842.751195080229, "a2_1": 0.0797604393422287, "b2_0": 394.62292870525204, "b2_1": 0.6141677387683908, "a3_0": 220.3248125148657, "a3_1": 0.018039276721954232, "b3_0": 4099.154370449441, "b3_1": 0.015638857739307885, "bh_0": 5.116339212581976, "bh_1": 1.5506489256388676, "bh_2": 0.18985417640438687, "ah_0": 0.15795441439869795, "ah_1": 16352.094042767683, "ah_2": 0.00289394098449451, "vShift": -36.512063968522256, "vShift_inact": 16.57598518131821, "maxrate": 14698.0057500302},
                        "2-mut2345_2_TTP3":{"a1_0": 297.0995472581599, "a1_1": 0.40453658405782256, "b1_0": 1.163250133004707, "b1_1": 0.007421955722949944, "a2_0": 6081.457375053355, "a2_1": 0.10901126825208024, "b2_0": 319.9492052219595, "b2_1": 3.695138405387749, "a3_0": 169.61349165235103, "a3_1": 0.002083746715518288, "b3_0": 2464.362441539251, "b3_1": 0.00726627005404204, "bh_0": 2.170829289387583, "bh_1": 2.213617474639907, "bh_2": 0.16880644254957078, "ah_0": 7.582754372567585, "ah_1": 66682.01097053559, "ah_2": 4.36251269415953e-05, "vShift": -34.67951312416439, "vShift_inact": 8.521648036537671, "maxrate": 2880.821073347662},
                        "2-mut2345_3_TTP3":{"a1_0": 502.0628023706877, "a1_1": 0.39719989447284576, "b1_0": 3.363118237030516, "b1_1": 0.22548890273027627, "a2_0": 8684.865776944864, "a2_1": 0.19029523308395643, "b2_0": 9.633532705350362, "b2_1": 0.36196830279533987, "a3_0": 224.6830260855691, "a3_1": 0.0035550343232721125, "b3_0": 4610.60168655902, "b3_1": 0.0032691294001463665, "bh_0": 1.7923264835470731, "bh_1": 0.19620936860204985, "bh_2": 0.1542552957138221, "ah_0": 37.941088908311905, "ah_1": 43600.400939319836, "ah_2": 0.012407463976142442, "vShift": -35.698526725684204, "vShift_inact": 17.779904111429936, "maxrate": 1025.5341769896756}}
                        #"2-mut2345_4_TTP3":{"a1_0": 207.64470710230637, "a1_1": 0.7085083922346641, "b1_0": 2.4833710546196754, "b1_1": 0.10878878927494169, "a2_0": 5736.50550473427, "a2_1": 0.03110050638797454, "b2_0": 667.1078129551366, "b2_1": 2.9273701803505747, "a3_0": 275.8980971267565, "a3_1": 2.2531738335012166e-05, "b3_0": 1508.5040521113108, "b3_1": 0.0008973433576946863, "bh_0": 6.423806285748963, "bh_1": 11.997225458600457, "bh_2": 0.1141409709393324, "ah_0": 3.8677545698202156, "ah_1": 501635.28883034113, "ah_2": 0.04568577758858561, "vShift": -39.41845166928241, "vShift_inact": 10.784920575012514, "maxrate": 41.19766655439892}}
                ###################### 12 ######################

                for mutname,dict in changesna12_071424mid.items():
                        print(f"mutname is {mutname}")
                        print(f"it's corresponding dictionary is {dict}")
                        nf.modify_dict_file(filename12,dict)
                        # nf.modify_dict_file(filename16,dict)

                        # i12a=i12/2
                        sim = tf.Na12Model_TF(ais_nav12_fac=24,ais_nav16_fac=3,nav12=i12,nav16=i16, somaK=1, KP=100, KT=1, #ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=50, KT=1, 15-6
                                        ais_ca = 10,ais_Kca = 10, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
                                        plots_folder = f'{root_path_out}/3-{mutname}_12-{i12}_16-{i16}', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
                        
                        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
                        plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                        fig_volts.savefig(f'{sim.plot_folder}/3-{mutname}_12-{i12}_16-{i16}.pdf')
                

                # ##Plotting WT vs Mut Stim/DVDT/FI/Currentscapes
                        sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'{mutname}-')#fnpre=f'{mutTXT}')
                        sim.make_currentscape_plot(amp=0.5, time1=100,time2=400,stim_start=100, sweep_len=800)
                        # sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)
                        # sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1075,stim_start=700, sweep_len=1200)
                













































#Make WT and save data for comparison later
                # sim = tf.Na12Model_TF(ais_nav12_fac=7,ais_nav16_fac = 7,nav12=4,nav16=3,somaK=i,na12name = 'na12_HMM_TF100923',mut_name = 'na12_HMM_TF100923',
                #                 na16mechs=['na16HH_TF','na16HH_TF'],params_folder = './params/na12HMM_allsynthmuts_HOFs/',
                #                 plots_folder = f'{root_path_out}/somaK-{i}', pfx=f'WT_')
                

                ##TF031424 Best params
                # sim = tf.Na12Model_TF(ais_nav12_fac=8,ais_nav16_fac=8,nav12=1,nav16=15, KT=i12,somaK=6,
                #                 na12name = 'na12_HMM_TF100923-2',mut_name = 'na12_HMM_TF100923-2',na12mechs = ['na12annaTFHH','na12annaTFHH'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16HH_TF','na16HH_TF'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}', pfx=f'WT_', update=False
                #                 )  #f'{root_path_out}/na12-{i12}_na16-{i16}'
                
                
                #################### HH MODEL ####################
                ##TF031924 These are the parameters that work best for 12HH16HH model!!!
                ##TF040224 Newly found best HH params following debugging of na12/16 and ais12/16 updating
                # sim = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=2,nav12=3,nav16=1, somaK=1, KP=100, KT=10, #somaK=10 KP=20, KP=90_KT=40
                #                         ais_ca = 1,ais_Kca = 1,soma_na16=1,soma_na12 = 1,node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40,
                #                 na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/1_na12-{i12}_na16-{i16}', pfx=f'WT_', update=True)
                #################### HH MODEL ####################


                
                ##TF040324 Different insufficiency experiments (50% het and 0% KO) HH model Het 50% and KO na12 everywhere (including ais)
                # simwt = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=2,nav12=3,nav16=1, somaK=1, KP=100, KT=10, #somaK=10 KP=20, KP=90_KT=40
                #                         ais_ca = 1,ais_Kca=1,soma_na16=1,soma_na12=1,node_na=1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40,
                #                         na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                #                         na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                         plots_folder = f'{root_path_out}/2_KO_na12', pfx=f'WT_', update=True)
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)

                #TF040424 Insert HMM and begin tuning
                # sim = tf.Na12Model_TF(ais_nav12_fac=1.5,ais_nav16_fac=1.5,nav12=2,nav16=2, somaK=1, KP=100, KT=1, #somaK=10  KP=14,KT=40, ais_nav12_fac=1.5,ais_nav16_fac=1.5,nav12=1,nav16=8, nav1216=2;5-10=1,7
                #                 ais_ca = 1,ais_Kca = 1, soma_na12=2, soma_na16=1, dend_nav12=1, node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                #                 na12name = 'na12_HMM_TF100923-2',mut_name = 'na12_HMM_TF100923-2',na12mechs = ['na12','na12mut'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/5-13-CaL0.5_SKE2-2_epas-85', pfx=f'WT_', update=True)
                






                ##TF061124 na16hmm params
                # changesna16a={"mut1_1": {"a1_0": 8.785465360653674, "a1_1": 0.11830586064228803, "b1_0": 42.12552904646244, "b1_1": 0.036697042766434894, "a2_0": 5865.576711787817, "a2_1": 0.11862977991276047, "b2_0": 44.560259619318884, "b2_1": 14.461613033140853, "a3_0": 342.4343505388412, "a3_1": 0.14302486015364324, "b3_0": 48.69456453744277, "b3_1": 0.06262750781938059, "bh_0": 15.972938277477665, "bh_1": 9.651217502394502, "bh_2": 0.15789378818961133, "ah_0": 0.5441915312192902, "ah_1": 170570.11887417815, "ah_2": 0.07822683312397283, "vShift": -2.8007320503043847, "vShift_inact": -7.378046425010265, "maxrate": 12.170479927592368},
                #         "mut12_3": {"a1_0": 9.985023142246815, "a1_1": 0.012967931001940006, "b1_0": 0.42174551350577494, "b1_1": 0.018343365198718445, "a2_0": 7623.026899534621, "a2_1": 5.190930667402921e-06, "b2_0": 43.06093761933944, "b2_1": 6.071819651436151, "a3_0": 1321.4472191146742, "a3_1": 0.2619024894347622, "b3_0": 49.41734982327105, "b3_1": 3.878478811025071e-05, "bh_0": 18.969735665542423, "bh_1": 5.447480328641684, "bh_2": 0.1103857694023778, "ah_0": 0.02277025295444523, "ah_1": 478227.41308455705, "ah_2": 0.15628327239137646, "vShift": -8.825525115465272, "vShift_inact": 17.889465440635348, "maxrate": 54.69031098814051},
                #         "mut3_1": {"a1_0": 7.490540556171526, "a1_1": 0.03968196576621144, "b1_0": 0.4797195445305464, "b1_1": 0.02819098724249631, "a2_0": 13391.272785556139, "a2_1": 0.11452580170501198, "b2_0": 45.053130647084004, "b2_1": 2.5164495071730753, "a3_0": 1376.561247270533, "a3_1": 0.26842134504835174, "b3_0": 49.80792875922528, "b3_1": 0.03875928742486645, "bh_0": 26.906261372515104, "bh_1": 2.550488381798932, "bh_2": 0.09654893016403679, "ah_0": 3.1009884813904285, "ah_1": 1683.4856359266194, "ah_2": 0.013796811271309613, "vShift": -9.133910320755733, "vShift_inact": 28.998778440008046, "maxrate": 19.801140035472116},
                #         "mut2_4": {"a1_0": 6.520876391823715, "a1_1": 0.05712719755542127, "b1_0": 1.3741913806966999, "b1_1": 0.01910207587066163, "a2_0": 8657.703022715139, "a2_1": 0.016956943029374293, "b2_0": 46.90757212777661, "b2_1": 0.20832255798611232, "a3_0": 90.67320052181867, "a3_1": 0.006923451122565546, "b3_0": 49.88062914542209, "b3_1": 0.12734602384605087, "bh_0": 3.8161867501706928, "bh_1": 10.07311020440889, "bh_2": 0.1316038307897467, "ah_0": 0.857478788378495, "ah_1": 22997.229806026946, "ah_2": 0.04809460875505616, "vShift": -6.852101028869071, "vShift_inact": -4.9103552523951555, "maxrate": 10919.634702982581},
                #         "mut3_3": {"a1_0": 9.951049462108125, "a1_1": 0.0419705503887564, "b1_0": 3.761998989874823, "b1_1": 0.004668801623497074, "a2_0": 8638.823052987931, "a2_1": 0.21834172088770276, "b2_0": 44.33804255425874, "b2_1": 5.118436038815119, "a3_0": 815.4256119705858, "a3_1": 0.25057295133527296, "b3_0": 45.75836417378028, "b3_1": 0.3306029825439243, "bh_0": 24.566197782791544, "bh_1": 6.371812965535927, "bh_2": 0.13643943097758612, "ah_0": 1.1137746084958096, "ah_1": 52256.70780840541, "ah_2": 0.05071452555663294, "vShift": -9.99657033591357, "vShift_inact": 10.596162824011197, "maxrate": 18.628436494303173},
                #         "mut12_2": {"a1_0": 9.469274321711952, "a1_1": 0.03342507474385595, "b1_0": 4.05008887854631, "b1_1": 0.02539852309193555, "a2_0": 7161.99059533367, "a2_1": 0.04551501372975401, "b2_0": 33.92222561429336, "b2_1": 37.900162148322494, "a3_0": 600.673279405948, "a3_1": 0.22088176955259076, "b3_0": 41.89959836920801, "b3_1": 0.00012527799445481713, "bh_0": 14.281670505688226, "bh_1": 21.67614396098298, "bh_2": 0.12321703638007638, "ah_0": 1.7658599715873378, "ah_1": 305994.74490546086, "ah_2": 0.06521706506031785, "vShift": -8.93787249928508, "vShift_inact": 3.3183603568955284, "maxrate": 20.536381791674277},
                #         "mut2_1": {"a1_0": 9.993229744609263, "a1_1": 0.0348008369058567, "b1_0": 0.5278376751103693, "b1_1": 0.053631050254988946, "a2_0": 5193.776125654254, "a2_1": 0.20365645338534108, "b2_0": 31.7180624800511, "b2_1": 6.290672031859296, "a3_0": 546.8784095816347, "a3_1": 0.12714919471813158, "b3_0": 47.85991294816933, "b3_1": 0.014518846926774836, "bh_0": 15.098145498712135, "bh_1": 3.4102340607521238, "bh_2": 0.11748344244695877, "ah_0": 1.2220428230760865, "ah_1": 52782.89013436118, "ah_2": 0.04843281708676325, "vShift": -7.3252955565800635, "vShift_inact": 20.48668878976599, "maxrate": 39.542146415711315},
                #         "mut4_3": {"a1_0": 7.370688908652268, "a1_1": 0.08506774783220702, "b1_0": 3.8276671379942084, "b1_1": 0.05261700468225406, "a2_0": 11524.263432737354, "a2_1": 0.1238027969941617, "b2_0": 28.66054298146001, "b2_1": 7.453874509803373, "a3_0": 379.7862892665614, "a3_1": 0.13024932827486, "b3_0": 49.99127754718318, "b3_1": 0.0026727885195541763, "bh_0": 14.494828235695637, "bh_1": 19.786002803074386, "bh_2": 0.15201349050572938, "ah_0": 1.6374671335956577, "ah_1": 164205.35847936437, "ah_2": 0.06739748770957318, "vShift": -9.98684647171616, "vShift_inact": 3.1407593828052507, "maxrate": 39.925271469478915},
                #         "mut2_2": {"a1_0": 5.839969207800412, "a1_1": 0.0241288001468336, "b1_0": 0.08729744098458841, "b1_1": 0.05608162488132777, "a2_0": 11785.290445184706, "a2_1": 0.02638367820026799, "b2_0": 43.83923831720964, "b2_1": 0.19045543703693113, "a3_0": 531.3806490991649, "a3_1": 0.1573447456587313, "b3_0": 49.99348722039813, "b3_1": 0.010949891803654715, "bh_0": 12.10509142488262, "bh_1": 4.419163378455123, "bh_2": 0.12773780227741716, "ah_0": 0.18129161320809906, "ah_1": 236558.92168209582, "ah_2": 0.07910376622177345, "vShift": -9.417825605792135, "vShift_inact": 11.513074558062986, "maxrate": 423.0696451505092},
                #         "mut9_2": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut2_3": {"a1_0": 9.95774934864715, "a1_1": 0.03664390832101938, "b1_0": 15.753360067241786, "b1_1": 0.03569893743088527, "a2_0": 5919.176352693952, "a2_1": 0.04083543558470672, "b2_0": 22.15746316043277, "b2_1": 1.6109128686802108, "a3_0": 845.3678723805933, "a3_1": 0.011745752125952774, "b3_0": 50.0, "b3_1": 0.0868166212261334, "bh_0": 18.20853059597512, "bh_1": 5.649265310074517, "bh_2": 0.1248442257778378, "ah_0": 0.7301888410108064, "ah_1": 66511.91106101929, "ah_2": 0.05856716165469785, "vShift": -10.0, "vShift_inact": 15.394476470257317, "maxrate": 7134.719839119786},
                #         "mut5_1": {"a1_0": 9.926882150099301, "a1_1": 0.018600189038124326, "b1_0": 14.41367791954432, "b1_1": 0.0013060692395693752, "a2_0": 7219.966825642858, "a2_1": 0.3011137756357386, "b2_0": 44.86111294072093, "b2_1": 52.177169325561294, "a3_0": 694.4465187943955, "a3_1": 0.01067596282380625, "b3_0": 38.4033870179841, "b3_1": 0.03733420342867269, "bh_0": 14.134876058734267, "bh_1": 5.952315793393123, "bh_2": 0.12193984521266475, "ah_0": 0.5369225879642185, "ah_1": 743921.5888339826, "ah_2": 0.08250116607269906, "vShift": -9.886030769239596, "vShift_inact": 13.71957810457647, "maxrate": 37.9576139479827},
                #         "mut8_2": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut10_1": {"a1_0": 9.103385555187224, "a1_1": 0.03783850434360721, "b1_0": 0.38742598625486013, "b1_1": 0.030267248666314545, "a2_0": 9888.597056894025, "a2_1": 0.3623039076124359, "b2_0": 43.09264072213054, "b2_1": 18.44760607210833, "a3_0": 204.26064809165328, "a3_1": 0.10525976451969495, "b3_0": 44.808969698012845, "b3_1": 0.06372029994752981, "bh_0": 11.25907195065116, "bh_1": 4.473778714261201, "bh_2": 0.11184341073074883, "ah_0": 2.1724573668995117, "ah_1": 4651.872083959752, "ah_2": 0.024479642017511592, "vShift": -10.0, "vShift_inact": 14.550793154053904, "maxrate": 30.613217292143965},
                #         "mut10_3": {"a1_0": 9.998204108959628, "a1_1": 0.021435867325549224, "b1_0": 0.2571825021209211, "b1_1": 0.032372287294653544, "a2_0": 6620.532127060434, "a2_1": 0.04278314946584192, "b2_0": 47.812079306899214, "b2_1": 0.749705429327626, "a3_0": 114.30857950181382, "a3_1": 0.25551209648756684, "b3_0": 47.56541498446684, "b3_1": 0.012408056787541803, "bh_0": 22.40253074460136, "bh_1": 23.42557839982356, "bh_2": 0.11709417018834851, "ah_0": 1.1360765612465418, "ah_1": 218530.8838894705, "ah_2": 0.06778632990008158, "vShift": -9.96827880331657, "vShift_inact": 8.728028423994557, "maxrate": 12.880317925194817},
                #         "mut5_4": {"a1_0": 7.11301887223947, "a1_1": 0.019753931102003804, "b1_0": 1.1970700211779342, "b1_1": 0.0015179378473516789, "a2_0": 9227.656908969413, "a2_1": 0.1997478756134971, "b2_0": 49.97798892996726, "b2_1": 4.663066780034374, "a3_0": 556.3878570438139, "a3_1": 0.15862572966176136, "b3_0": 43.173996561414114, "b3_1": 0.0008007041045655292, "bh_0": 3.2252919427647333, "bh_1": 1.138611359469441, "bh_2": 0.1152575047133852, "ah_0": 1.711748730998036, "ah_1": 1139.4452329176315, "ah_2": 0.01979820969332307, "vShift": -9.999904750880914, "vShift_inact": 5.110704096720006, "maxrate": 362.7545710496905},
                #         "mut5_2": {"a1_0": 9.711378815685665, "a1_1": 0.015480330254980856, "b1_0": 0.13675477744410802, "b1_1": 0.02984564263588966, "a2_0": 9391.521520076145, "a2_1": 0.3568848133708977, "b2_0": 43.01037326562896, "b2_1": 0.058445136693892175, "a3_0": 39.314366163176324, "a3_1": 0.007656560544101669, "b3_0": 46.58981095552915, "b3_1": 0.004604731761626006, "bh_0": 41.21559856096876, "bh_1": 17.731891754732438, "bh_2": 0.12026200352958631, "ah_0": 0.19358045366336357, "ah_1": 58232.67355719084, "ah_2": 0.06304449365211531, "vShift": -8.557051712118522, "vShift_inact": 13.588704717176261, "maxrate": 761.1008711962359},
                #         "mut7_4": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut3_2": {"a1_0": 9.961588651658793, "a1_1": 0.11264675833375554, "b1_0": 1.153628639501905, "b1_1": 0.014822111449329883, "a2_0": 12925.866584639505, "a2_1": 0.2160055569353333, "b2_0": 42.29018658483371, "b2_1": 0.3577619443877462, "a3_0": 3825.002699530089, "a3_1": 0.3133421620198351, "b3_0": 12.927786060281658, "b3_1": 0.027676121638993217, "bh_0": 20.99737123493846, "bh_1": 5.810496525065096, "bh_2": 0.11545186246427352, "ah_0": 3.7961978046749567, "ah_1": 306801.8565167909, "ah_2": 0.051566022701973024, "vShift": -9.420505021121762, "vShift_inact": 20.792332756595542, "maxrate": 20.99041430869237},
                #         "mut3_4": {"a1_0": 6.737586765017045, "a1_1": 0.04106288645115188, "b1_0": 17.924468456255518, "b1_1": 0.0379050301179346, "a2_0": 9169.064945005013, "a2_1": 0.32159699963997584, "b2_0": 49.746574505314165, "b2_1": 0.6687720753490218, "a3_0": 927.4454207373201, "a3_1": 0.05742188644711062, "b3_0": 25.132393751775375, "b3_1": 0.008035240447986584, "bh_0": 12.187986769887218, "bh_1": 12.482478239609529, "bh_2": 0.12623135346394007, "ah_0": 0.08073440089583686, "ah_1": 167310.36308464565, "ah_2": 0.09089552763753148, "vShift": -9.829880015065873, "vShift_inact": 6.949850893876079, "maxrate": 32.04775528118261},
                #         "mut7_2": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut7_3": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut8_3": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut12_1": {"a1_0": 9.643482762163599, "a1_1": 0.011677592613265259, "b1_0": 0.14525389079641648, "b1_1": 0.054978593028128075, "a2_0": 8752.193804407814, "a2_1": 0.3600722091851446, "b2_0": 25.913118791656157, "b2_1": 0.9990877400956335, "a3_0": 534.664946041601, "a3_1": 0.03853335311938105, "b3_0": 40.49756918493545, "b3_1": 0.3524649586145831, "bh_0": 23.531308808004297, "bh_1": 8.516300875946925, "bh_2": 0.12501391385305255, "ah_0": 1.3717336989993467, "ah_1": 11849.01702676127, "ah_2": 0.04231046936686679, "vShift": -9.100533886523868, "vShift_inact": 10.469138642892283, "maxrate": 26.04897887101447},
                #         "mut10_4": {"a1_0": 8.0578874919151, "a1_1": 0.0362460004441742, "b1_0": 0.2975424360004787, "b1_1": 0.019626504231602726, "a2_0": 7541.367908495317, "a2_1": 0.008115928598620786, "b2_0": 37.78264401293287, "b2_1": 13.197541674645006, "a3_0": 2661.4548837273387, "a3_1": 0.28322186815760786, "b3_0": 41.45025415671522, "b3_1": 0.005946538949708524, "bh_0": 4.957064052666118, "bh_1": 14.94315170855162, "bh_2": 0.10627633864486724, "ah_0": 0.3348261287268917, "ah_1": 1847.8521286814391, "ah_2": 0.04174076351521052, "vShift": -9.569584432015834, "vShift_inact": 2.352045239220809, "maxrate": 44.84946684890218},
                #         "mut9_1": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut6_3": {"a1_0": 2.003841798041574, "a1_1": 0.01107476233163529, "b1_0": 1.7975168702185822, "b1_1": 0.02984876907893916, "a2_0": 5342.4019544606745, "a2_1": 0.19457512713351763, "b2_0": 50.0, "b2_1": 0.7105958385012334, "a3_0": 219.04908962167477, "a3_1": 0.042669754497766096, "b3_0": 48.14324766346968, "b3_1": 0.029429113230670868, "bh_0": 22.497627738488507, "bh_1": 2.5417760359411483, "bh_2": 0.13582850875839206, "ah_0": 0.8668500069097885, "ah_1": 109609.02787570507, "ah_2": 0.031771855034601164, "vShift": -8.827113711526342, "vShift_inact": 16.55862996857032, "maxrate": 300.15648855113704},
                #         "mut7_1": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut10_2": {"a1_0": 2.5874621107358964, "a1_1": 0.05251855720358095, "b1_0": 18.899560854232504, "b1_1": 0.04464380804426573, "a2_0": 5048.760629223852, "a2_1": 0.006621347964626193, "b2_0": 50.0, "b2_1": 0.0054958474266508794, "a3_0": 365.17704184383496, "a3_1": 0.11550827801285289, "b3_0": 40.873820434932625, "b3_1": 0.010010873384021401, "bh_0": 20.238578071331208, "bh_1": 10.459587400720864, "bh_2": 0.12279292388483401, "ah_0": 0.20843531857105557, "ah_1": 1304578.8844524745, "ah_2": 0.0932503292109903, "vShift": -6.440459583714217, "vShift_inact": 8.89240168792451, "maxrate": 1462.9314553184422},
                #         "mut11_4": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut6_1": {"a1_0": 7.9845010929337885, "a1_1": 0.012185780483391452, "b1_0": 0.022507535723755634, "b1_1": 0.07158849510143048, "a2_0": 3305.5535174935703, "a2_1": 0.27405145304901257, "b2_0": 49.999356520081434, "b2_1": 52.564205397777926, "a3_0": 2679.6811013299184, "a3_1": 0.2607204762199863, "b3_0": 45.144294049658804, "b3_1": 0.29754517525325774, "bh_0": 20.75964228434551, "bh_1": 19.836431501008914, "bh_2": 0.11996038744260666, "ah_0": 0.46056119456857103, "ah_1": 25628.472062967063, "ah_2": 0.0633873422513562, "vShift": -7.745108648055127, "vShift_inact": 4.750456070722582, "maxrate": 18.816396483730816},
                #         "mut8_4": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut5_3": {"a1_0": 7.888342367385148, "a1_1": 0.046593131765013784, "b1_0": 7.786374367082527, "b1_1": 0.055435265569232325, "a2_0": 10719.695555229571, "a2_1": 0.09669662118142176, "b2_0": 30.00802151350781, "b2_1": 24.154341265158, "a3_0": 583.5720334598967, "a3_1": 0.28961759466039294, "b3_0": 43.20351634541398, "b3_1": 0.011801754809243298, "bh_0": 2.2755529690556733, "bh_1": 6.684472414262677, "bh_2": 0.14823684111433333, "ah_0": 4.97336720100144, "ah_1": 151755.51971909593, "ah_2": 0.06049933840866869, "vShift": -9.771577576024594, "vShift_inact": -8.928555508304411, "maxrate": 13.091989256699696},
                #         "mut11_2": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut11_1": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut4_2": {"a1_0": 7.806535336213503, "a1_1": 0.031855202861343045, "b1_0": 0.6761697681664209, "b1_1": 0.09714582934164682, "a2_0": 11514.503459471534, "a2_1": 0.1624237747665157, "b2_0": 48.510668199512395, "b2_1": 0.10021242834581612, "a3_0": 42.176977493828986, "a3_1": 0.019943150495713928, "b3_0": 48.428574158471356, "b3_1": 0.0004913637032166705, "bh_0": 18.244996873075984, "bh_1": 9.276131644176404, "bh_2": 0.0933372697983346, "ah_0": 0.023752982099336684, "ah_1": 3183.154006275867, "ah_2": 0.08259768430129504, "vShift": -6.431368927811262, "vShift_inact": 13.511033674784855, "maxrate": 30943.97867449208},
                #         "mut4_4": {"a1_0": 7.444509387622613, "a1_1": 0.002403969931539726, "b1_0": 0.47694916911736907, "b1_1": 0.09500795948225024, "a2_0": 5640.114916134273, "a2_1": 0.03292387225125637, "b2_0": 45.26234499053626, "b2_1": 0.18705902937992036, "a3_0": 83.82490069753817, "a3_1": 0.07308745564392678, "b3_0": 41.28297703527208, "b3_1": 0.013461596647817556, "bh_0": 6.440669435094437, "bh_1": 5.972049852902967, "bh_2": 0.14337011010314776, "ah_0": 1.4139130947020304, "ah_1": 2039.7138463206575, "ah_2": 0.02989192320012601, "vShift": -9.99856366928063, "vShift_inact": 3.766390679999071, "maxrate": 4574.19558090576},
                #         "mut1_3": {"a1_0": 8.402833398126516, "a1_1": 0.060282421379415446, "b1_0": 7.506838052948601, "b1_1": 0.017625103169249673, "a2_0": 9891.508670867339, "a2_1": 0.038846504498082385, "b2_0": 49.23137059320615, "b2_1": 2.8498225935043564, "a3_0": 1075.4958398153024, "a3_1": 0.07262982113778867, "b3_0": 49.994942485071476, "b3_1": 0.04753123280013827, "bh_0": 29.60564570850853, "bh_1": 3.6097238323196823, "bh_2": 0.12493590989849887, "ah_0": 2.7432331125999676, "ah_1": 16943.173387318006, "ah_2": 0.02798952236709104, "vShift": -9.613938020064872, "vShift_inact": 24.4841986289971, "maxrate": 3188.004591113213},
                #         "mut6_4": {"a1_0": 2.003841798041574, "a1_1": 0.01107476233163529, "b1_0": 1.7975168702185822, "b1_1": 0.02984876907893916, "a2_0": 5342.4019544606745, "a2_1": 0.19457512713351763, "b2_0": 50.0, "b2_1": 0.7105958385012334, "a3_0": 219.04908962167477, "a3_1": 0.042669754497766096, "b3_0": 48.14324766346968, "b3_1": 0.029429113230670868, "bh_0": 22.497627738488507, "bh_1": 2.5417760359411483, "bh_2": 0.13582850875839206, "ah_0": 0.8668500069097885, "ah_1": 109609.02787570507, "ah_2": 0.031771855034601164, "vShift": -8.827113711526342, "vShift_inact": 16.55862996857032, "maxrate": 300.15648855113704},
                #         "mut9_4": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut8_1": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut1_2": {"a1_0": 8.760481453868328, "a1_1": 0.04394320003403557, "b1_0": 0.6876520284180163, "b1_1": 0.06325234714405, "a2_0": 4556.962008666881, "a2_1": 0.04111072080092468, "b2_0": 31.88058948179966, "b2_1": 1.567771786249177, "a3_0": 84.49969614421335, "a3_1": 0.16012046025119292, "b3_0": 49.126279429079645, "b3_1": 0.021070832854345502, "bh_0": 17.463274736373698, "bh_1": 5.630815081284107, "bh_2": 0.1135010448192984, "ah_0": 2.787632469386511, "ah_1": 4530.328802475745, "ah_2": 0.026689408042462535, "vShift": -10.0, "vShift_inact": 13.599453367806117, "maxrate": 19.120771967848448},
                #         "mut11_3": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528},
                #         "mut1_4": {"a1_0": 7.127013407167688, "a1_1": 0.0004387243673637173, "b1_0": 0.453481281559229, "b1_1": 0.03949503149403946, "a2_0": 13689.39033669123, "a2_1": 0.019943336284361193, "b2_0": 40.990399532067386, "b2_1": 5.324564269581929, "a3_0": 1962.6130085799696, "a3_1": 0.0223781555366054, "b3_0": 46.76500854850627, "b3_1": 0.16578555680497714, "bh_0": 6.419028633058257, "bh_1": 5.521408669624966, "bh_2": 0.11344496805289245, "ah_0": 2.6837632768984285, "ah_1": 11718.443094917668, "ah_2": 0.031381877106846735, "vShift": -9.926219013163797, "vShift_inact": 10.280325139830245, "maxrate": 32443.072243183524},
                #         "mut4_1": {"a1_0": 6.7699522573173265, "a1_1": 0.03434337105132962, "b1_0": 4.031864591255902, "b1_1": 0.0010748728098553169, "a2_0": 6667.398838806432, "a2_1": 0.3006582698431951, "b2_0": 44.587174683582276, "b2_1": 0.059668986864582774, "a3_0": 260.1654724813962, "a3_1": 0.04115449628092851, "b3_0": 47.870947791499916, "b3_1": 0.07903525228465547, "bh_0": 13.142582291031486, "bh_1": 4.517211655728241, "bh_2": 0.09942784533762868, "ah_0": 1.1547350937288665, "ah_1": 62828.44034616856, "ah_2": 0.047147446497569814, "vShift": -9.57591478819121, "vShift_inact": 18.130862027806323, "maxrate": 49.78846221722419},
                #         "mut6_2": {"a1_0": 6.282779004564331, "a1_1": 0.015418183042892275, "b1_0": 0.3412275279393877, "b1_1": 0.02874964506505005, "a2_0": 768.8493942116938, "a2_1": 0.16219648185341928, "b2_0": 49.99994744816823, "b2_1": 28.09782993594852, "a3_0": 2071.916769598935, "a3_1": 0.20811350027148234, "b3_0": 45.53563194201337, "b3_1": 0.1470364732658037, "bh_0": 28.36361124918497, "bh_1": 17.644016851515214, "bh_2": 0.1230209899827839, "ah_0": 0.4699731119582266, "ah_1": 50706.7876482177, "ah_2": 0.05247534156066454, "vShift": -5.893736382595451, "vShift_inact": 7.689392687033132, "maxrate": 19.031319002560632},
                #         "mut9_3": {"a1_0": 6.985057948951453, "a1_1": 0.0009969051935738577, "b1_0": 0.9401480231095742, "b1_1": 0.014525981156654003, "a2_0": 2478.570121625588, "a2_1": 0.15550429434484986, "b2_0": 36.69666916966754, "b2_1": 1.2832251057479047, "a3_0": 235.04756719664655, "a3_1": 0.15822979122251674, "b3_0": 46.360560055666014, "b3_1": 0.006801087309639477, "bh_0": 69.65527011828804, "bh_1": 9.318766546005174, "bh_2": 0.11975240347468774, "ah_0": 0.7270246328507318, "ah_1": 10292.876913644584, "ah_2": 0.03827798092887311, "vShift": -8.713539083415501, "vShift_inact": 20.268555937178512, "maxrate": 43.08038651534528}}
















        ###  Make directories with names from list in txt file (mutant_names.txt)
        # file = open('/global/homes/t/tfenton/Neuron_general-2/JUPYTERmutant_list.txt','r')
        # Lines = file.readlines()
        # for line in Lines:
        #         print (line)
        #         mutTXT = line.strip()
        #         path = os.path.join(root_path_out,mutTXT)
        #         # if not os.path.exists(path):
        #         #         os.mkdir(path)

        #         print (mutTXT)
        #         print(line)



        #         sim = tf.Na12Model_TF(ais_nav12_fac=7, ais_nav16_fac=7, nav12=4, nav16=3,na12name = 'na12_HMM_TF100923',mut_name = mutTXT+'_121123',
        #                         params_folder = './params/na12HMM_allsynthmuts_HOFs/',
        #                         plots_folder = f'{root_path_out}/{mutTXT}_', pfx=f'{mutTXT}_')


        #         #make spiking and dvdt plots
        #         # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm,wt_t=wt_t,vs_amp=[0.5], fnpre=f'{mutTXT}_Na16-{i16}')
                
        #         #soma
        #         sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'{mutTXT}_')
        #         #features_df = ef.get_features(sim=sim,mutTXT=f'{root_path_out}/{mutTXT}_{i}-nav16', mut_name = mutTXT+'_121123')

        #         #make currentscape plots
        #         # sim.make_currentscape_plot(amp=0.5, time1=25,time2=60,stim_start=30, sweep_len=75)
        #         sim.make_currentscape_plot(amp=0.5, time1=0,time2=100,stim_start=30, sweep_len=100)
        #         # sim.make_currentscape_plot(amp=0.5, time1=0,time2=250,stim_start=30, sweep_len=300)

        #################################################################################
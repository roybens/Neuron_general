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


root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/Restart030824/5-12HMM16HH_040324/10-debug'

if not os.path.exists(root_path_out):
        os.makedirs(root_path_out)
        # os.mkdir(root_path_out)


vals =[1]#[1]#[-80,-70-60,-50,-40,-30]
vals2 = [1]#[-30,-40,-50,-60,-70,-80]#[1]

# for i12 in np.arange(1,2,3):     
#       for i16 in np.arange(1,2,3):
for i12 in vals:
        for i16 in vals2:
                ##Adding below function to loop through different na16.mod params        
                # filename = "/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TF100923-2.txt" ##TF031524 for changing 8st na12
                filename12 = '/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TF100923-2.txt'
                filename16 = '/global/homes/t/tfenton/Neuron_general-2/params/na16HH_TF2.txt'

                # changesna12 = {
                #         "sh": 8,#-3#i12,#8,
                #         "gbar": 0.01,#0.06,#0.1,#0.01,
                #         "tha": -30,#i12,#-38,
                #         "qa": 5.41,
                #         "Ra": 0.3282,
                #         "Rb": 0.1,
                #         "thi1": -40,#-80,
                #         "thi2": -40,#-80,
                #         "qd": 0.5,
                #         "qg": 1.5,
                #         "mmin": 0.02,
                #         "hmin": 0.01,
                #         "Rg": 0.01,
                #         "Rd": 0.02657,
                #         "thinf": -53,
                #         "qinf": 7.69,
                #         "vhalfs": -60,
                #         "a0s": 0.0003,
                #         "gms": 0.2,
                #         "q10": 2,
                #         "zetas": 12,
                #         "smax": 10,
                #         "vvh": -58,
                #         "vvs": 2,
                #         "ar2": 1,
                #         #"ena": 55
                #         }
                changesna16 = {
                        "sh": 8,#-3,#i16,#8,
                        "gbar": 0.01,#0.06,#0.1,#0.01,
                        "tha": -40,#-47,
                        "qa": 7.2,
                        "Ra": 0.4,
                        "Rb": 0.124,
                        "thi1": -30,#-61,
                        "thi2": -30,#-61,
                        "qd": 0.5,
                        "qg": 1.5,
                        "mmin": 0.02,  
                        "hmin": 0.01,  
                        "q10": 2,
                        "Rg": 0.01,
                        "Rd": 0.03,
                        "thinf": -65,
                        "qinf": 7,
                        "vhalfs": -40,
                        "a0s": 0.0003,
                        "gms": 0.2,
                        "zetas": 12,
                        "smax": 10,
                        "vvh": -58,
                        "vvs": 2,
                        "ar2": 1,
                        #"ena": 55
                        }
                ##TF042324 vshifted WT-HMM
                # changesna12 = {"a1_0": 7.3917081233326964, 
                #         "a1_1": 0.020960637742640235, 
                #         "b1_0": 0.36296088733379755, 
                #         "b1_1": 0.16680524810129632, 
                #         "a2_0": 466.03560625002507, 
                #         "a2_1": 0.32567824887881647, 
                #         "b2_0": 476.76246431747546, 
                #         "b2_1": 3.237964775220791, 
                #         "a3_0": 138.3653253992877, 
                #         "a3_1": 0.1294574328268014, 
                #         "b3_0": 3569.9158743150915, 
                #         "b3_1": 0.0872001126087137, 
                #         "bh_0": 2.431699390098816, 
                #         "bh_1": 4.764311256848339, 
                #         "bh_2": 0.12976195895416504, 
                #         "ah_0": 3.640921294365118, 
                #         "ah_1": 5944.063823249113, 
                #         "ah_2": 0.019988765965544244, 
                #         "vShift": -30, #-22.94301368173753, 
                #         "vShift_inact":20, # 17.286867168698212, 
                #         "maxrate": 2233.5902391087598
                #         }
                
                ##TF042324 mut10_1 fit from vshifted wt-HMM
                changesna12 = {"a1_0": 47.88395304510355, 
                        "a1_1": 0.580116333776531, 
                        "b1_0": 2.1736548357107743, 
                        "b1_1": 0.0736381407276879, 
                        "a2_0": 11589.631011535717, 
                        "a2_1": 0.11575919917484359, 
                        "b2_0": 317.2921388390646, 
                        "b2_1": 1.300066280406203, 
                        "a3_0": 260.3693108979363, 
                        "a3_1": 0.1819905691948297, 
                        "b3_0": 3613.6839364554876, 
                        "b3_1": 0.14316250229426114, 
                        "bh_0": 8.434406038655029, 
                        "bh_1": 6.544547121753995, 
                        "bh_2": 0.14512358801027536, 
                        "ah_0": 1.9718027694081248, 
                        "ah_1": 45953.40255162975, 
                        "ah_2": 0.044087424752603, 
                        "vShift": -24.26233946779172, 
                        "vShift_inact": 19.212301660453747, 
                        "maxrate": 554.4854193940364}
                
                ##TF042324 mut2_1 fit from vshifted wt_HMM
                # changesna12 = {"a1_0": 190.06546985816848, 
                #         "a1_1": 0.866341360844602, 
                #         "b1_0": 3.1817435275724484, 
                #         "b1_1": 0.1797666932720414, 
                #         "a2_0": 10752.857233895027, 
                #         "a2_1": 0.3096729051119419, 
                #         "b2_0": 439.95573025519104, 
                #         "b2_1": 2.837183904388915, 
                #         "a3_0": 413.9219734776599, 
                #         "a3_1": 0.09066501592163359, 
                #         "b3_0": 2747.78507120295, 
                #         "b3_1": 0.025723311731907117, 
                #         "bh_0": 7.919984499615688, 
                #         "bh_1": 4.411282666300695, 
                #         "bh_2": 0.1528009419610445, 
                #         "ah_0": 0.7646502286075908, 
                #         "ah_1": 180986.53143078965, 
                #         "ah_2": 0.05314974687147448, 
                #         "vShift": -24.491850165626715, 
                #         "vShift_inact": 20.305932384104505, 
                #         "maxrate": 811.3775517272184}
                
                ##TF042324 mut4_4 fit from vshifted wt_HMM
                # changesna12 = {"a1_0": 145.3169910688194, 
                #         "a1_1": 0.6892020856372565, 
                #         "b1_0": 0.38672830773824507, 
                #         "b1_1": 0.16650947924561554, 
                #         "a2_0": 16551.333021772734, 
                #         "a2_1": 0.049091612851463774, 
                #         "b2_0": 259.65922911272656, 
                #         "b2_1": 2.8045436864586497, 
                #         "a3_0": 321.70172239261854, 
                #         "a3_1": 0.17665389590962516, 
                #         "b3_0": 3020.9909048322015, 
                #         "b3_1": 0.13197003788859388, 
                #         "bh_0": 4.607724878304812, 
                #         "bh_1": 6.775624011953492, 
                #         "bh_2": 0.2409471679688329, 
                #         "ah_0": 7.7929851680262585, 
                #         "ah_1": 5817.166189708863, 
                #         "ah_2": 0.024443708362379628, 
                #         "vShift": -21.619498121793203, 
                #         "vShift_inact": 4.223380991503497, 
                #         "maxrate": 606.9565956119159}
                
                ##TF042324 mut10_4 fit from vshifted wt_HMM
                # changesna12 = {"a1_0": 109.87667115259035, 
                #         "a1_1": 0.6079261865917412, 
                #         "b1_0": 4.113095593538036, 
                #         "b1_1": 0.0016895429443995911, 
                #         "a2_0": 14476.82556036098, 
                #         "a2_1": 0.2256529959703877, 
                #         "b2_0": 164.01836269706186, 
                #         "b2_1": 2.616310409196042, 
                #         "a3_0": 287.61843669903556, 
                #         "a3_1": 0.08506019620282235, 
                #         "b3_0": 2015.836184382626, 
                #         "b3_1": 0.10904828877170832, 
                #         "bh_0": 10.505928535174931, 
                #         "bh_1": 8.876021203632611, 
                #         "bh_2": 0.14530016999117046, 
                #         "ah_0": 3.149343231350516, 
                #         "ah_1": 23349.315592258383, 
                #         "ah_2": 0.04019999923739183, 
                #         "vShift": -28.632365908741107, 
                #         "vShift_inact": 21.594055794626733, 
                #         "maxrate": 11773370.716274362}
                ##Uncomment if want to update params file to update mod file!!!
                nf.modify_dict_file(filename12, changesna12)
                nf.modify_dict_file(filename16, changesna16)

 

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
                
                ##TF042324 replace hmmWT with mut10_1 to account for different Tau0's in HH vs HMM vclamp act/inact/tau0 plots
                sim = tf.Na12Model_TF(ais_nav12_fac=1.5,ais_nav16_fac=1.5,nav12=2,nav16=0.5, somaK=1, KP=100, KT=1, #somaK=10  KP=14, KT=40, ais_nav12_fac=1.5,ais_nav16_fac=1.5,nav12=1,nav16=8, nav1216=2;5-10=1,7
                                ais_ca = 1,ais_Kca = 1, soma_na12=2, soma_na16=1, dend_nav12=1, node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                                na12name = 'mut10_1_12HMM_042324',mut_name = 'mut10_1_12HMM_042324',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/5-vals-{i12}{i16}', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
                
                                
                fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue')
                plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                fig_volts.savefig(f'{sim.plot_folder}/5-vals-{i12}{i16}.pdf')
                # plt.clf()
                
                # sim.save2text(ais_nav12_fac=8,ais_nav16_fac=i16,nav12=1,nav16=15,
                #                 na12name = 'na12_HMM_TF100923-2',mut_name = 'na12_HMM_TF100923-2',na12mechs = ['na12annaTFHH','na12annaTFHH'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16HH_TF','na16HH_TF'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/gbar.01_1216-115_ais88_KP-{i12}----TEST')

                ##Plotting WT vs Mut Stim/DVDT/FI/Currentscapes
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'12-{i12}_16-{i16}_')#fnpre=f'{mutTXT}')
                # # # features_df = ef.get_features(sim=sim,mutTXT='WT_soma', mut_name = 'na12_HMM_TF100923')  
                
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=100,stim_start=30, sweep_len=100)
                sim.make_currentscape_plot(amp=0.5, time1=0,time2=200,stim_start=30, sweep_len=200)
                sim.make_currentscape_plot(amp=0.5, time1=0,time2=800,stim_start=30, sweep_len=800)



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
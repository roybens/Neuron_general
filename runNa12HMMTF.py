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


root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/Restart030824/6-HMM_focusonTTP_042624/8-12HMMmut10_459101112_TTP8_050224'

if not os.path.exists(root_path_out):
        os.makedirs(root_path_out)
        # os.mkdir(root_path_out)


vals =[1]#[-80,-70-60,-50,-40,-30]
vals2 = [1]#[-30,-40,-50,-60,-70,-80]#[1]

# for i12 in np.arange(2,3,1):     
#       for i16 in np.arange(7,8,1):
for i12 in vals:
        for i16 in vals2:
                ##Adding below function to loop through different na16.mod params        
                # filename = "/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TF100923-2.txt" ##TF031524 for changing 8st na12
                filename12 = '/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TEMP_PARAMS.txt'
                filename16 = '/global/homes/t/tfenton/Neuron_general-2/params/na16HH_TF2.txt'

                ##HH model
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
                
                ##16HH
                changesna16 = {
                        "sh": 8,
                        "gbar": 0.01,
                        "tha": -40, #noshift=-40,
                        "qa": 7.2,
                        "Ra": 0.4,
                        "Rb": 0.124,
                        "thi1": -30,#noshift=-30,
                        "thi2": -30,#noshift=-30,
                        "qd": 0.5,
                        "qg": 1.5,
                        "mmin": 0.02,  
                        "hmin": 0.01,  
                        "q10": 2,
                        "Rg": 0.01,
                        "Rd": 0.03,
                        "thinf": -65,#noshift=-65,
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
                    
                
                

                ##mut10_4_TTP8 043024
                # changesna12={"a1_0": 76.53693049713668, 
                #         "a1_1": 0.58467481812683, 
                #         "b1_0": 8.862327698663911, 
                #         "b1_1": 0.027795796031250652, 
                #         "a2_0": 3308.274658619428, 
                #         "a2_1": 0.16523236331162441, 
                #         "b2_0": 367.9732263854306, 
                #         "b2_1": 1.3317361363431022, 
                #         "a3_0": 73.19056812685912, 
                #         "a3_1": 0.0661688859750417, 
                #         "b3_0": 2283.2554509507595, 
                #         "b3_1": 0.3337501059568756, 
                #         "bh_0": 0.9630015061711104, 
                #         "bh_1": 4.335694369456647, 
                #         "bh_2": 0.12228161756894262, 
                #         "ah_0": 3.78837998891378, 
                #         "ah_1": 10222.772037890725, 
                #         "ah_2": 0.0343298286662707, 
                #         "vShift": -20.438350564204057, 
                #         "vShift_inact": 6.854888556940034, 
                #         "maxrate": 11.69263400283082}
                
                ##mut10_4_TTP8 050224
                # changesna12={"a1_0": 1.625145083336028, "a1_1": 0.0034044338446176936, "b1_0": 0.7716064184650755, "b1_1": 0.22900894014243406, "a2_0": 4494.856286467831, "a2_1": 0.484202536750758, "b2_0": 490.19586610910204, "b2_1": 2.965468694039672, "a3_0": 160.60824167776218, "a3_1": 0.07738922515916669, "b3_0": 3388.25425524152, "b3_1": 0.17827564344360108, "bh_0": 0.2792118983951942, "bh_1": 1.4922526025309482, "bh_2": 0.1431979487525067, "ah_0": 3.379887929381378, "ah_1": 47610.365258567195, "ah_2": 0.03735815022515161, "vShift": -27.237391062521564, "vShift_inact": 9.674622767295796, "maxrate": 1360.4209516807975}
                # ##mut10_5_TTP8 050224, can't run because of NaN
                # changesna12={"a1_0": 1.201477564539962, "a1_1": NaN, "b1_0": 1.4250275435765847, "b1_1": 0.2439950542335529, "a2_0": 8915.248028941143, "a2_1": 0.27980316192180227, "b2_0": NaN, "b2_1": 0.02038421214050401, "a3_0": 124.04505908067078, "a3_1": 0.1450032902711169, "b3_0": 4355.898374489158, "b3_1": 0.21968286991084143, "bh_0": 1.1737180103106937, "bh_1": 9.982906484406671, "bh_2": 0.12680947331011708, "ah_0": 1.8619678200518603, "ah_1": 192883.94639790483, "ah_2": 0.09633685661253664, "vShift": -26.865356056990183, "vShift_inact": 10.0737328029312, "maxrate": 1470.381367268004}
                # ##mut10_6_TTP8 050224
                # changesna12={"a1_0": 121.8694549248113, "a1_1": 0.5152068909165036, "b1_0": 8.24645031554915, "b1_1": 0.03948492175790076, "a2_0": 8603.062471049778, "a2_1": 0.0007059278863327245, "b2_0": 437.031568683939, "b2_1": 1.1181731385438813, "a3_0": 227.4059510050261, "a3_1": 0.026550857351707778, "b3_0": 2478.1177916782603, "b3_1": 0.15738504991805988, "bh_0": 4.549259878057603, "bh_1": 6.541504339956773, "bh_2": 0.13199929709998992, "ah_0": 0.7793483835555817, "ah_1": 12294.081045839595, "ah_2": 0.03428149373801122, "vShift": -19.295958478564692, "vShift_inact": 14.812010831320269, "maxrate": 127.11131875367822}
                # ##mut10_7_TTP8 050224
                # changesna12={"a1_0": 1.516144143773679, "a1_1": 0.00393322454881892, "b1_0": 4.71222597902555, "b1_1": 0.21030816800589636, "a2_0": 8719.009166938084, "a2_1": 0.001980803440951917, "b2_0": 394.16125271706113, "b2_1": 0.03589303732514926, "a3_0": 208.91584589371698, "a3_1": 0.12791274377291875, "b3_0": 4121.370196239627, "b3_1": 0.05015090922577167, "bh_0": 0.3812179736436594, "bh_1": 6.554773265201365, "bh_2": 0.12379097248582452, "ah_0": 9.079564195875456, "ah_1": 220486.37824416102, "ah_2": 0.04358517014119633, "vShift": -24.550327766804863, "vShift_inact": 3.1366910296171167, "maxrate": 1452.5618118163145}
                ##mut10_8_TTP8 050224
                # changesna12={"a1_0": 1.1960547963668346, "a1_1": 0.07223909928923195, "b1_0": 0.3257001611251462, "b1_1": 0.024776714856335008, "a2_0": 8074.163036993882, "a2_1": 0.003321406185837119, "b2_0": 71.36995906226485, "b2_1": 0.9427529191150504, "a3_0": 213.17840761221342, "a3_1": 0.3164503707522971, "b3_0": 4325.074455438461, "b3_1": 0.09807397355159038, "bh_0": 0.19761769133831864, "bh_1": 2.9151760388882115, "bh_2": 0.15456675299405798, "ah_0": 1.0851539007746032, "ah_1": 111616.4611544509, "ah_2": 0.03231239852867908, "vShift": -26.552859291788042, "vShift_inact": 0.9501183834304237, "maxrate": 1387.3953611760396}
                #mut10_9_TTP8 050224 midopt3hr
                # changesna12={"a1_0": 20.738270571725597, "a1_1": 0.3886703764344085, "b1_0": 1.7777657212116993, "b1_1": 0.07133880391845333, "a2_0": 13738.752894030553, "a2_1": 0.001072434705231412, "b2_0": 316.67344931792195, "b2_1": 2.259989170117984, "a3_0": 244.7527462755213, "a3_1": 0.12579717339767021, "b3_0": 3128.4818314898152, "b3_1": 0.03983978451064088, "bh_0": 1.1794987814522668, "bh_1": 3.0406715641209985, "bh_2": 0.1386771747691053, "ah_0": 1.2034863037905796, "ah_1": 162725.3723019725, "ah_2": 0.06330126798417667, "vShift": -16.010025990356915, "vShift_inact": 5.31092545822662, "maxrate": 9.70064278311512}


                #mut10_459101112_TTP8 12hr runs 050324 
                #mut10_4_TTP8
                # changesna12={"a1_0": 160.88212172270394, "a1_1": 0.37740904747898113, "b1_0": 7.809034143930841, "b1_1": 0.3598403604885581, "a2_0": 9582.19328693931, "a2_1": 0.007479049352698795, "b2_0": 494.496826417892, "b2_1": 0.7903838804543639, "a3_0": 245.47934538123076, "a3_1": 0.23252657753436962, "b3_0": 483.57294559282826, "b3_1": 0.06386641433443244, "bh_0": 0.230620429966387, "bh_1": 0.31284169413359064, "bh_2": 0.13876006467360502, "ah_0": 0.008209871274113434, "ah_1": 210574.17829531862, "ah_2": 0.10668056235141984, "vShift": -13.594570818511734, "vShift_inact": 8.043483113572183, "maxrate": 7.729422229296069}
                # #mut10_5_TTP8
                # changesna12={"a1_0": 204.08010208894942, "a1_1": 0.8040966665776965, "b1_0": 3.421855706270912, "b1_1": 0.04812849172653662, "a2_0": 8004.280577858399, "a2_1": 0.039816198746696216, "b2_0": 364.81222370387326, "b2_1": 4.4856030468960295, "a3_0": 283.52085472948534, "a3_1": 0.05040415941799445, "b3_0": 4679.8811922045525, "b3_1": 0.08606976926568045, "bh_0": 6.371676928979497, "bh_1": 5.731582755135726, "bh_2": 0.13311142600164094, "ah_0": 8.040725824188588, "ah_1": 52789.476083567206, "ah_2": 0.00880145101862833, "vShift": -21.729341423924396, "vShift_inact": 20.334090276585535, "maxrate": 686.1362775908706}
                # #mut10_9_TTP8
                # changesna12={"a1_0": 20.738270571725597, "a1_1": 0.3886703764344085, "b1_0": 1.7777657212116993, "b1_1": 0.07133880391845333, "a2_0": 13738.752894030553, "a2_1": 0.001072434705231412, "b2_0": 316.67344931792195, "b2_1": 2.259989170117984, "a3_0": 244.7527462755213, "a3_1": 0.12579717339767021, "b3_0": 3128.4818314898152, "b3_1": 0.03983978451064088, "bh_0": 1.1794987814522668, "bh_1": 3.0406715641209985, "bh_2": 0.1386771747691053, "ah_0": 1.2034863037905796, "ah_1": 162725.3723019725, "ah_2": 0.06330126798417667, "vShift": -16.010025990356915, "vShift_inact": 5.31092545822662, "maxrate": 9.70064278311512}
                # #mut10_10_TTP8
                # changesna12={"a1_0": 25.628435448437912, "a1_1": 0.6253666513768823, "b1_0": 0.712858742262038, "b1_1": 0.18160138739589263, "a2_0": 9436.95014218921, "a2_1": 0.2963356870477131, "b2_0": 403.32713508543156, "b2_1": 2.4671144912588803, "a3_0": 240.04730584446688, "a3_1": 0.11071078501277484, "b3_0": 1708.2200311504787, "b3_1": 0.03535781309753684, "bh_0": 5.149917919366038, "bh_1": 3.953768557392907, "bh_2": 0.1474660984257752, "ah_0": 1.194712453680853, "ah_1": 15913.643440591506, "ah_2": 0.045524076397265786, "vShift": -24.002739074774002, "vShift_inact": 18.380712257182754, "maxrate": 847.8534978407606}
                # #mut10_11_TTP8
                # changesna12={"a1_0": 303.82186157592844, "a1_1": 0.8057265764516777, "b1_0": 2.0325911600965068, "b1_1": 0.00703045910364021, "a2_0": 8506.042398419393, "a2_1": 0.04132215332958844, "b2_0": 365.9541884051876, "b2_1": 0.7947075667089529, "a3_0": 342.18234581184703, "a3_1": 0.16691892598229055, "b3_0": 4915.516352968663, "b3_1": 0.10141070716929047, "bh_0": 6.977936955801824, "bh_1": 6.572242121277074, "bh_2": 0.13311142600164094, "ah_0": 8.371555984260002, "ah_1": 50974.696880907926, "ah_2": 0.020751604240623174, "vShift": -20.855465346135812, "vShift_inact": 18.10875859692538, "maxrate": 686.1362775908706}
                # #mut10_12_TTP8
                changesna12={"a1_0": 95.70801317669665, "a1_1": 0.869609530944387, "b1_0": 3.011028429230476, "b1_1": 0.12148888744920948, "a2_0": 9467.538859037928, "a2_1": 0.05069924707277115, "b2_0": 328.70674342570953, "b2_1": 2.805835221891905, "a3_0": 236.46741316843074, "a3_1": 0.03888384499371427, "b3_0": 2742.8853120606755, "b3_1": 0.12424599531853064, "bh_0": 3.6883548795186276, "bh_1": 5.757168810270557, "bh_2": 0.1491082064678782, "ah_0": 0.49678697695149676, "ah_1": 19760.477056402495, "ah_2": 0.04503014445432112, "vShift": -25.144371628489367, "vShift_inact": 15.22740056713415, "maxrate": 314.18976984743983}

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
                sim = tf.Na12Model_TF(ais_nav12_fac=1,ais_nav16_fac=1,nav12=2,nav16=7, somaK=1, KP=100, KT=1, #somaK=10  KP=14,100 KT=40, ais_nav12_fac=1.5,ais_nav16_fac=1.5,nav12=1,nav16=8, nav1216=2;5-10=1,7, 12=2 16=0.5
                                ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/6-mut1012_TTP8-baseline', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
                
                                
                fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
                plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                fig_volts.savefig(f'{sim.plot_folder}/6-mut1012_TTP8-baseline.pdf')
                
                # sim.save2text(ais_nav12_fac=8,ais_nav16_fac=i16,nav12=1,nav16=15,
                #                 na12name = 'na12_HMM_TF100923-2',mut_name = 'na12_HMM_TF100923-2',na12mechs = ['na12annaTFHH','na12annaTFHH'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16HH_TF','na16HH_TF'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/gbar.01_1216-115_ais88_KP-{i12}----TEST')

                ##Plotting WT vs Mut Stim/DVDT/FI/Currentscapes
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'12-{i12}_16-{i16}_')#fnpre=f'{mutTXT}')
                # # # features_df = ef.get_features(sim=sim,mutTXT='WT_soma', mut_name = 'na12_HMM_TF100923')  
                
                # sim.plot_fi_curve(start=0,end=2,nruns=21,wt_data = None,ax1 = None, fig = None,fn = 'ficurve')
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=100,stim_start=30, sweep_len=100)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=200,stim_start=30, sweep_len=200)
                sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)
                sim.make_currentscape_plot(amp=0.5, time1=600,time2=1200,stim_start=700, sweep_len=1200)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=1200,stim_start=700, sweep_len=1200)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=500,stim_start=500, sweep_len=1000)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=500,stim_start=600, sweep_len=1000)
                # sim.make_currentscape_plot(amp=0.5, time1=860,time2=890,stim_start=700, sweep_len=1000) #single AP




        #####Other 1.2 params
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
                # changesna12 = {"a1_0": 47.88395304510355, 
                #         "a1_1": 0.580116333776531, 
                #         "b1_0": 2.1736548357107743, 
                #         "b1_1": 0.0736381407276879, 
                #         "a2_0": 11589.631011535717, 
                #         "a2_1": 0.11575919917484359, 
                #         "b2_0": 317.2921388390646, 
                #         "b2_1": 1.300066280406203, 
                #         "a3_0": 260.3693108979363, 
                #         "a3_1": 0.1819905691948297, 
                #         "b3_0": 3613.6839364554876, 
                #         "b3_1": 0.14316250229426114, 
                #         "bh_0": 8.434406038655029, 
                #         "bh_1": 6.544547121753995, 
                #         "bh_2": 0.14512358801027536, 
                #         "ah_0": 1.9718027694081248, 
                #         "ah_1": 45953.40255162975, 
                #         "ah_2": 0.044087424752603, 
                #         "vShift": -24.26233946779172, 
                #         "vShift_inact": 19.212301660453747, 
                #         "maxrate": 554.4854193940364}
                
                              
                
                ##TF042524 midpoint mut10_1_TTP
                # changesna12 = {"a1_0": 325.82132647120443, 
                #         "a1_1": 0.2823364001168773, 
                #         "b1_0": 2.0600534638020545, 
                #         "b1_1": 0.006741533596643143, 
                #         "a2_0": 2733.181770421286, 
                #         "a2_1": 0.31918802152813075, 
                #         "b2_0": 333.9496497287754, 
                #         "b2_1": 1.2450427744838526, 
                #         "a3_0": 200.83277051453084, 
                #         "a3_1": 0.5993153362905674, 
                #         "b3_0": 263.8673987731195, 
                #         "b3_1": 0.2181663577728353, 
                #         "bh_0": 0.5037524698414151, 
                #         "bh_1": 1.6417757853800001, 
                #         "bh_2": 0.18481853346350516, 
                #         "ah_0": 0.04403812666974849, 
                #         "ah_1": 33921.98354506484, 
                #         "ah_2": 0.04558915358587949, 
                #         "vShift": -20.84587866899704, 
                #         "vShift_inact": 0.14965748560416348, 
                #         "maxrate": 9.662637162476162}

                ############################################
                ##TF042624 mut10_1_TTPs
                ##mut10_1_TTP1
                # changesna12 = {"a1_0": 133.6880815248557, 
                #         "a1_1": 0.15750190164594055, 
                #         "b1_0": 1.5477805645098683, 
                #         "b1_1": 0.0068187654362214314, 
                #         "a2_0": 692.3416303430263, 
                #         "a2_1": 0.41335125591942956, 
                #         "b2_0": 352.0267173066926, 
                #         "b2_1": 1.9175215094639708, 
                #         "a3_0": 246.4143184213077, 
                #         "a3_1": 0.03693051576691639, 
                #         "b3_0": 2299.5510233698656, 
                #         "b3_1": 0.11724423289016316, 
                #         "bh_0": 6.21892751315144, 
                #         "bh_1": 3.2935535272576746, 
                #         "bh_2": 0.15011425989762517, 
                #         "ah_0": 0.8744510900223859, 
                #         "ah_1": 129667.86927240732, 
                #         "ah_2": 0.053474167828359405, 
                #         "vShift": -22.737061316613442, 
                #         "vShift_inact": 20.097026006797172, 
                #         "maxrate": 457.7093669051503}
                
                # ##mut10_1_TTP2
                # changesna12 = {"a1_0": 156.0063282016801, 
                #         "a1_1": 1.4718989540329193, 
                #         "b1_0": 2.9087171530544573, 
                #         "b1_1": 0.06237855317495, 
                #         "a2_0": 19343.962944357838, 
                #         "a2_1": 0.02764049825517205, 
                #         "b2_0": 189.5926861437827, 
                #         "b2_1": 3.7186586756804574, 
                #         "a3_0": 158.75524568919124, 
                #         "a3_1": 0.16257124455313685, 
                #         "b3_0": 4359.058015304009, 
                #         "b3_1": 0.0750987652229112, 
                #         "bh_0": 2.2530281748939665, 
                #         "bh_1": 9.918412209135383, 
                #         "bh_2": 0.14603829631585752, 
                #         "ah_0": 0.7530251783006805, 
                #         "ah_1": 5472.649575796222, 
                #         "ah_2": 0.04386060535576493, 
                #         "vShift": -27.980556032063756, 
                #         "vShift_inact": 9.676709732952052, 
                #         "maxrate": 1064.131438073359}

                ##mut10_1_TTP3
                # changesna12={"a1_0": 418.24576208132817, 
                #         "a1_1": 0.3720449609907387, 
                #         "b1_0": 2.0770486847636875, 
                #         "b1_1": 0.22909996330404103, 
                #         "a2_0": 27412.691156982422, 
                #         "a2_1": 0.5764854576601492, 
                #         "b2_0": 270.2190074083039, 
                #         "b2_1": 2.127385231227855, 
                #         "a3_0": 332.09225090848645, 
                #         "a3_1": 0.6035104572575214, 
                #         "b3_0": 139.83013051073405, 
                #         "b3_1": 0.2724879430618975, 
                #         "bh_0": 0.5037524698414151, 
                #         "bh_1": 3.955954530095854, 
                #         "bh_2": 0.10032413943194227, 
                #         "ah_0": 4.6488939475974576, 
                #         "ah_1": 9974.897174235135, 
                #         "ah_2": 0.058723844359627665, 
                #         "vShift": -20.29277001925661, 
                #         "vShift_inact": 2.0997366874857146, 
                #         "maxrate": 5.486358933293742}

                ##mut10_1_TTP4 and 5 couldn't run because they contained NaN values                        
                ##mut10_1_TTP6
                # changesna12={"a1_0": 0.20016108568135493, 
                #         "a1_1": 0.001062057306080822, 
                #         "b1_0": 2.852573771414524, 
                #         "b1_1": 0.47878973821725923, 
                #         "a2_0": 9625.570335693394, 
                #         "a2_1": 0.008583814034756321, 
                #         "b2_0": 421.33450625914634, 
                #         "b2_1": 1.298126493787385, 
                #         "a3_0": 402.25304680211116, 
                #         "a3_1": 0.15964052283282387, 
                #         "b3_0": 3051.732576007426, 
                #         "b3_1": 0.06417576626687892, 
                #         "bh_0": 0.023679719966860108, 
                #         "bh_1": 1.161559715502811, 
                #         "bh_2": 0.44722009759990394, 
                #         "ah_0": 2.624731782227725, 
                #         "ah_1": 24352.91030013184, 
                #         "ah_2": 0.08399920338496607,
                #         "vShift": -31.76378910393356, 
                #         "vShift_inact": 1.9898981489197345, 
                #         "maxrate": 439518092.1825677}          
                
                ##mut10_1_TTP7
                # changesna12={"a1_0": 0.16540681819264264, 
                #         "a1_1": 0.005066383213086827, 
                #         "b1_0": 0.6270314013836054,
                #         "b1_1": 0.08263337237927382,
                #         "a2_0": 50077.16110764631, 
                #         "a2_1": 0.12437577049061342, 
                #         "b2_0": 208.8441227148926, 
                #         "b2_1": 1.5316913496039688, 
                #         "a3_0": 96.87390167622796, 
                #         "a3_1": 8.408692325628797e-06, 
                #         "b3_0": 640.5919315366953, 
                #         "b3_1": 0.24654620748932798, 
                #         "bh_0": 0.06049092613139173, 
                #         "bh_1": 0.001666570012147206, 
                #         "bh_2": 0.22270626882583217, 
                #         "ah_0": 0.7959141049540349, 
                #         "ah_1": 81768.8189174333, 
                #         "ah_2": 0.08493256872348842, 
                #         "vShift": -29.156751719202735, 
                #         "vShift_inact": 24.125276556394926, 
                #         "maxrate": 719884070.459955}         
                
                ##mut10_1_TTP9 4hr mid optimization
                # changesna12={"a1_0": 1.477814526433131, 
                #         "a1_1": 0.01,#10#0, 
                #         "b1_0": 0.8036876626408171, 
                #         "b1_1": 0.0025732146687779903, 
                #         "a2_0": 420.6989600555271, 
                #         "a2_1": 0.035570635198289735, 
                #         "b2_0": 334.4360152639672, 
                #         "b2_1": 2.090573622150073, 
                #         "a3_0": 187.98818801332968, 
                #         "a3_1": 0.04588407856547343, 
                #         "b3_0": 2624.745677018715, 
                #         "b3_1": 0.09614812211746718, 
                #         "bh_0": 1.14680176395072, 
                #         "bh_1": 10.0, 
                #         "bh_2": 0.1456003107484689, 
                #         "ah_0": 7.39068884463619, 
                #         "ah_1": 253493.1719437468, 
                #         "ah_2": 0.06557058594794697, 
                #         "vShift": -30.939128945867555, 
                #         "vShift_inact": 9.04707875663167, 
                #         "maxrate": 39161325.69160889}   
                
                # ##mut10_1_TTP10 
                # changesna12={"a1_0": 104.78855355174372, 
                #         "a1_1": 0.06644997516781687, 
                #         "b1_0": 5.261566157360312, 
                #         "b1_1": 0.4333296857889514, 
                #         "a2_0": 32871.95234017431, 
                #         "a2_1": 0.15524877667965786, 
                #         "b2_0": 445.2058906002243, 
                #         "b2_1": 3.7594137557591023, 
                #         "a3_0": 343.8871650021617, 
                #         "a3_1": 0.5154992105257559, 
                #         "b3_0": 1089.0356622819972, 
                #         "b3_1": 0.41514651879522335, 
                #         "bh_0": 0.7391184855657198, 
                #         "bh_1": 2.078398566970971, 
                #         "bh_2": 0.15148140651016734, 
                #         "ah_0": 1.0460090718822546, 
                #         "ah_1": 77361.2649480339, 
                #         "ah_2": 0.025203569929348524, 
                #         "vShift": -18.409704952528518, 
                #         "vShift_inact": 3.378032554153597, 
                #         "maxrate": 6.204334451476724}

# ##mut10_1_TTP8 
                # changesna12={"a1_0": 5.525835976869644, 
                #         "a1_1": 0.0386797348496386, 
                #         "b1_0": 2.1607926527581407, 
                #         "b1_1": 0.02902812310822782, 
                #         "a2_0": 2798.0494435232135, 
                #         "a2_1": 0.28679270567723547, 
                #         "b2_0": 371.28873642113484, 
                #         "b2_1": 0.6560068630072168, 
                #         "a3_0": 105.31276402049836, 
                #         "a3_1": 0.5409329610210727, 
                #         "b3_0": 312.8930164540953, 
                #         "b3_1": 0.1778994245901206, 
                #         "bh_0": 0.7295113632439284, 
                #         "bh_1": 4.74900548848539, 
                #         "bh_2": 0.13442502242110105, 
                #         "ah_0": 2.8338740227181547, 
                #         "ah_1": 77252.47148393965, 
                #         "ah_2": 0.035383529005003723, 
                #         "vShift": -21.301775592151373, 
                #         "vShift_inact": 4.013505166345816, 
                #         "maxrate": 20.980538721558936}

                ##mut10_2_TTP8 043024
                # changesna12={"a1_0": 171.2169998926389, 
                #         "a1_1": 0.017673809954567965, 
                #         "b1_0": 5.851013756922709, 
                #         "b1_1": 0.3142219393023481, 
                #         "a2_0": 26.13473174447362, 
                #         "a2_1": 0.19985211359883104, 
                #         "b2_0": 375.4226914476126, 
                #         "b2_1": 0.04030331026470546, 
                #         "a3_0": 124.05861482875002, 
                #         "a3_1": 0.59639481340742, 
                #         "b3_0": 108.44459596788309, 
                #         "b3_1": 0.16557847579371232, 
                #         "bh_0": 0.5751367996150408, 
                #         "bh_1": 5.920429455360875, 
                #         "bh_2": 0.1538324957161896, 
                #         "ah_0": 1.2629948566559304, 
                #         "ah_1": 216218.20746165363, 
                #         "ah_2": 0.013874750551409274, 
                #         "vShift": -23.552841113057905, 
                #         "vShift_inact": 0.1940724735015973, 
                #         "maxrate": 12.996493113532054}
                
                ##mut10_3_TTP8 043024
                # changesna12={"a1_0": 167.48685253475472, 
                #         "a1_1": 0.09174875571274349, 
                #         "b1_0": 5.537450955111864, 
                #         "b1_1": 0.502955876192051, 
                #         "a2_0": 23162.012517077415, 
                #         "a2_1": 0.14828127450021833, 
                #         "b2_0": 433.8056346428809, 
                #         "b2_1": 0.8002275876991375, 
                #         "a3_0": 169.53253885717857, 
                #         "a3_1": 0.4795948576921847, 
                #         "b3_0": 1133.8001151604406, 
                #         "b3_1": 0.3501763592136549, 
                #         "bh_0": 1.7620786815224267, 
                #         "bh_1": 3.63767544410417, 
                #         "bh_2": 0.12204112201874856, 
                #         "ah_0": 4.639693232883573, 
                #         "ah_1": 25236.39754683731, 
                #         "ah_2": 0.03462000046225626, 
                #         "vShift": -19.903605765770727, 
                #         "vShift_inact": 13.664900628263222, 
                #         "maxrate": 9.707077803973862}























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
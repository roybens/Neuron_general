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


root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/Restart030824/10-12HMM_wt_and_muts'
# root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HMM/1-Baselines052124'

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
                # filename12a = '/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TEMP_PARAMS2.txt'
                filename16 = '/global/homes/t/tfenton/Neuron_general-2/params/na16HH_TF2.txt'

                
                ##16HH
                changesna16 = {
                        "sh": 8,
                        # "gbar": 0.01,
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
                
                ##TF050824 mut10_9_TTP8 (from 050224) best WT so far
                # changesna12={"a1_0": 20.738270571725597, 
                #         "a1_1": 0.3886703764344085, 
                #         "b1_0": 1.7777657212116993, 
                #         "b1_1": 0.07133880391845333, 
                #         "a2_0": 13738.752894030553, 
                #         "a2_1": 0.001072434705231412, 
                #         "b2_0": 316.67344931792195, 
                #         "b2_1": 2.259989170117984, 
                #         "a3_0": 244.7527462755213, 
                #         "a3_1": 0.12579717339767021, 
                #         "b3_0": 3128.4818314898152, 
                #         "b3_1": 0.03983978451064088, 
                #         "bh_0": 1.1794987814522668, 
                #         "bh_1": 3.0406715641209985, 
                #         "bh_2": 0.1386771747691053, 
                #         "ah_0": 1.2034863037905796, 
                #         "ah_1": 162725.3723019725, 
                #         "ah_2": 0.06330126798417667, 
                #         "vShift": -16.010025990356915, 
                #         "vShift_inact": 5.31092545822662, 
                #         "maxrate": 9.70064278311512}
                              
                ##TF052024 mut10_12_TTP8 (from 050624) better WT (fit to mut10_9_TTP8)
                # changesna12={"a1_0": 62.774771313021546, 
                #         "a1_1": 0.6854152336583206,
                #         "b1_0": 3.2117067311143277,
                #         "b1_1": 0.1432460480232296, 
                #         "a2_0": 2468.966900014909,
                #         "a2_1": 0.0834387238328, 
                #         "b2_0": 490.16060600231606,
                #         "b2_1": 2.969500725999265,
                #         "a3_0": 190.5883640336242,
                #         "a3_1": 0.003108395956123883,
                #         "b3_0": 7689.251014289831, 
                #         "b3_1": 0.04054164070835632,
                #         "bh_0": 4.063594186259147,
                #         "bh_1": 2.115884898210715, 
                #         "bh_2": 0.1433653421971472,
                #         "ah_0": 1.3563238605774417,
                #         "ah_1": 6568.351916792737, 
                #         "ah_2": 0.011127551783912584,
                #         "vShift": -18.276678986708095, 
                #         "vShift_inact": 16.74204011921361, 
                #         "maxrate": 6.170113221706686}
                
                changesna12a = {"a1_0": 62.774771313021546,"a1_1": 0.6854152336583206,"b1_0": 3.2117067311143277,"b1_1": 0.1432460480232296, "a2_0": 2468.966900014909,"a2_1": 0.0834387238328, "b2_0": 490.16060600231606,"b2_1": 2.969500725999265,"a3_0": 190.5883640336242,"a3_1": 0.003108395956123883,"b3_0": 7689.251014289831, "b3_1": 0.04054164070835632,"bh_0": 4.063594186259147,"bh_1": 2.115884898210715, "bh_2": 0.1433653421971472,"ah_0": 1.3563238605774417,"ah_1": 6568.351916792737, "ah_2": 0.011127551783912584,"vShift": -18.276678986708095, "vShift_inact": 16.74204011921361, "maxrate": 6.170113221706686}                
                nf.modify_dict_file(filename12, changesna12a)
                nf.modify_dict_file(filename16, changesna16)
                
                simwt = tf.Na12Model_TF(ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=100, KT=1, 
                                        ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                        plots_folder = f'{root_path_out}/3-WT', pfx=f'WT_', update=True)
                wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                
                ##TF052224 Mutants for Scn2a grant and Migraine Stuff
                changesna12 = {
                "m1012ttp8":{"a1_0": 62.774771313021546,"a1_1": 0.6854152336583206,"b1_0": 3.2117067311143277,"b1_1": 0.1432460480232296, "a2_0": 2468.966900014909,"a2_1": 0.0834387238328, "b2_0": 490.16060600231606,"b2_1": 2.969500725999265,"a3_0": 190.5883640336242,"a3_1": 0.003108395956123883,"b3_0": 7689.251014289831, "b3_1": 0.04054164070835632,"bh_0": 4.063594186259147,"bh_1": 2.115884898210715, "bh_2": 0.1433653421971472,"ah_0": 1.3563238605774417,"ah_1": 6568.351916792737, "ah_2": 0.011127551783912584,"vShift": -18.276678986708095, "vShift_inact": 16.74204011921361, "maxrate": 6.170113221706686},
                "M1879T":{"a1_0": 171.65404967593912, "a1_1": 1.5473325780407043, "b1_0": 0.15668688284445786, "b1_1": 0.056578266862296, "a2_0": 10626.926411489329, "a2_1": 0.00041480337573633966, "b2_0": 29.048765867503395, "b2_1": 2.3342903358554383, "a3_0": 249.39252673373483, "a3_1": 0.0007503117414607886, "b3_0": 3066.9638504829777, "b3_1": 0.0188555817486158, "bh_0": 2.040068926358947, "bh_1": 3.7675241580162835, "bh_2": 0.02942144917704831, "ah_0": 0.4337041832768786, "ah_1": 6129.875372384539, "ah_2": 0.19871362195779174, "vShift": -16.853808606641802, "vShift_inact": 16.23871522904293, "maxrate": 147.56435592144186},
                "F257I":{"a1_0": 57.23222656544356, "a1_1": 0.5162476539537184, "b1_0": 1.8724690877184815, "b1_1": 0.3489228884827919, "a2_0": 6511.174812425784, "a2_1": 0.31511083304771054, "b2_0": 13.931212257800585, "b2_1": 3.549602963154167, "a3_0": 56.06617645856018, "a3_1": 0.20253982835842732, "b3_0": 4557.794989159212, "b3_1": 0.10663558594679154, "bh_0": 7.710006832717681, "bh_1": 14.572356290822542, "bh_2": 0.18368832756574835, "ah_0": 13.135285500451904, "ah_1": 582694.8911257205, "ah_2": 0.02450775477624999, "vShift": -14.790198857295309, "vShift_inact": 2.5986463273723643, "maxrate": 5.6664026906358025},
                "R1319G":{"a1_0": 11.725759655362136, "a1_1": 0.6571531403024519, "b1_0": 3.0065976174556512, "b1_1": 0.000902768010717224, "a2_0": 1742.7495829655707, "a2_1": 0.02251125633593753, "b2_0": 614.4646768407794, "b2_1": 0.8050557697779577, "a3_0": 15.468721657456264, "a3_1": 0.32793109120367053, "b3_0": 373.37385954192274, "b3_1": 0.05757001644645299, "bh_0": 2.2549687674388137, "bh_1": 6.916265330343567, "bh_2": 0.14921327138251256, "ah_0": 5.65060809152757, "ah_1": 45547.750321981424, "ah_2": 0.013818403982389392, "vShift": -19.406600254786213, "vShift_inact": 6.25935187673563, "maxrate": 8.684150279900209},
                "K1480E":{"a1_0": 307.00465576071645, "a1_1": 0.49198920082186476, "b1_0": 5.4276811512377, "b1_1": 0.4969838847492478, "a2_0": 22407.406708905273, "a2_1": 0.06296552204807644, "b2_0": 563.8533209681815, "b2_1": 0.4087458667615537, "a3_0": 225.3447082584479, "a3_1": 0.07259909061390746, "b3_0": 1335.942117834803, "b3_1": 0.023939088443790713, "bh_0": 11.240863085795546, "bh_1": 3.944597572625594, "bh_2": 0.13803337916549033, "ah_0": 10.560716200998332, "ah_1": 27038.18935249356, "ah_2": 0.014812167953595981, "vShift": -9.845708608417436, "vShift_inact": 15.305677325325039, "maxrate": 7.30690132513435},
                }

                # ##TF050824 mut10_5-13 fit to mut10_9_TTP8.
                # changesna12={"mut10_1":{"a1_0": 559.7395419475644, "a1_1": 1.6118947252237623, "b1_0": 5.796942895005852, "b1_1": 0.20673060819899028, "a2_0": 295.4715442119816, "a2_1": 0.12537078916956412, "b2_0": 430.8313126896239, "b2_1": 1.7648077505728925, "a3_0": 129.7287050319431, "a3_1": 0.0003735690025623176, "b3_0": 2352.673950047887, "b3_1": 0.0016281043181984676, "bh_0": 6.9512171030939225, "bh_1": 19.216471399067036, "bh_2": 0.14912604559884945, "ah_0": 5.31458071865826, "ah_1": 370404.9184628065, "ah_2": 0.033066372644917824, "vShift": -20.863377868930726, "vShift_inact": 7.165301442401468, "maxrate": 6.347893802473519},
                # "mut10_2":{"a1_0": 233.5849496343501, "a1_1": 1.1100362570504334, "b1_0": 5.817733516942724, "b1_1": 0.031198631197451615, "a2_0": 15143.165012586116, "a2_1": 0.5253983534312439, "b2_0": 354.8420877055062, "b2_1": 3.5709646528595798, "a3_0": 33.07985840619355, "a3_1": 0.27741220332436495, "b3_0": 2256.9955010874014, "b3_1": 0.05062650609669392, "bh_0": 9.165928629678628, "bh_1": 16.02677567882732, "bh_2": 0.14053201555721923, "ah_0": 0.5466576076284593, "ah_1": 6625.452699667287, "ah_2": 0.010092354464189518, "vShift": -20.158401170349244, "vShift_inact": 11.40838113481485, "maxrate": 5.205532628717714},
                # "mut10_5":{"a1_0": 0.8175962816429524, "a1_1": 0.03121588205834508, "b1_0": 0.0744746673948754, "b1_1": 0.11132158830492389, "a2_0": 13204.230002229458, "a2_1": 0.29183830413118095, "b2_0": 210.59427221114564, "b2_1": 3.0076977989068494, "a3_0": 433.53933597234834, "a3_1": 0.6042865823792669, "b3_0": 3694.1850011718543, "b3_1": 0.0043361248255975905, "bh_0": 5.138776755600741, "bh_1": 21.03421879541667, "bh_2": 0.1541931680140676, "ah_0": 4.895667727252144, "ah_1": 582713.9019979399, "ah_2": 0.040828796941040836, "vShift": -23.553779671048197, "vShift_inact": 5.959082612067263, "maxrate": 545.0549385972084},
                # "mut10_11":{"a1_0": 217.7764882719917, "a1_1": 1.2612334352408952, "b1_0": 0.5846218025336629, "b1_1": 0.13370425308851036, "a2_0": 3579.742201167344, "a2_1": 0.07315956734123634, "b2_0": 278.64110430289185, "b2_1": 2.5734484894546816, "a3_0": 67.88169140957082, "a3_1": 0.0023832979960251707, "b3_0": 1866.4702456069604, "b3_1": 0.008044061686699893, "bh_0": 14.065066558610647, "bh_1": 16.476536049649454, "bh_2": 0.1556431137159366, "ah_0": 7.810470437910962, "ah_1": 36495.04445494566, "ah_2": 0.012812791696751438, "vShift": -19.684977985113353, "vShift_inact": 9.35822463506868, "maxrate": 17.048642602049483},
                # "mut10_12":{"a1_0": 176.82754568537737, "a1_1": 1.1357123544748395, "b1_0": 2.716494618885052, "b1_1": 0.13496978675965182, "a2_0": 9644.440337089069, "a2_1": 0.2492458066485585, "b2_0": 327.19664715810313, "b2_1": 1.1440846054390899, "a3_0": 299.0379432813013, "a3_1": 0.12257136273310859, "b3_0": 1150.4174072857923, "b3_1": 0.08681076091384185, "bh_0": 8.375925558464942, "bh_1": 18.515986245733306, "bh_2": 0.1519784204033135, "ah_0": 47.30457040561784, "ah_1": 448381.62379709654, "ah_2": 0.016367957467689927, "vShift": -20.274284848494048, "vShift_inact": 6.641397859744719, "maxrate": 8.538014017714168},
                # "mut13_1":{"a1_0": 9.61468854373711, "a1_1": 0.63981735119507, "b1_0": 1.7708324593790925, "b1_1": 0.023252185072425338, "a2_0": 9086.760726813287, "a2_1": 0.04981931506718382, "b2_0": 517.5253863068335, "b2_1": 0.10061755767827041, "a3_0": 224.8874692275083, "a3_1": 0.001215260894700042, "b3_0": 3363.2649329253763, "b3_1": 0.0026626146982529925, "bh_0": 3.7683611073069807, "bh_1": 6.080192020592501, "bh_2": 0.1467600345973244, "ah_0": 14.108869399629521, "ah_1": 109128.48087846422, "ah_2": 0.016707452916454046, "vShift": -21.8070807327557, "vShift_inact": 11.453832052991128, "maxrate": 304.29965555183276},
                # "mut13_3":{"a1_0": 123.43590257466111, "a1_1": 0.9606706486679034, "b1_0": 1.6544526887443052, "b1_1": 0.5190803459628421, "a2_0": 8860.792503037395, "a2_1": 0.0259152951385715, "b2_0": 515.986001609208, "b2_1": 2.6720256115529626, "a3_0": 149.918074999944, "a3_1": 0.47244003927961853, "b3_0": 5760.358980957602, "b3_1": 0.003643199440391494, "bh_0": 2.7749126097624224, "bh_1": 10.477612485756303, "bh_2": 0.1425274562050642, "ah_0": 8.518223439905217, "ah_1": 61681.313529365114, "ah_2": 0.01879634480614487, "vShift": -19.514832178707998, "vShift_inact": 4.70034350103844, "maxrate": 3.653930459320725},
                # "mut2_1":{"a1_0": 33.69160414401048, "a1_1": 1.0409215382949943, "b1_0": 1.553890894354734, "b1_1": 0.4639646325911135, "a2_0": 833.6652202705059, "a2_1": 0.36213493264117974, "b2_0": 190.30475567949446, "b2_1": 6.6825415217044615, "a3_0": 60.75221805509284, "a3_1": 0.025256117763653566, "b3_0": 323.9549695047979, "b3_1": 0.0003950070087891779, "bh_0": 5.902835214676092, "bh_1": 14.706918666512493, "bh_2": 0.1647337851792094, "ah_0": 4.060160699409881, "ah_1": 332276.7106774799, "ah_2": 0.06852037308608006, "vShift": -23.823948323504787, "vShift_inact": 7.568979360707896, "maxrate": 4.45678670690157},
                # # 
                # }


                ##TF052324 set for debugging unk=unknown for temp debugging                
                # changesna12 = {
                # "unk3_garb":{"a1_0": 76.53693049713668, "a1_1": 0.58467481812683,"b1_0": 8.862327698663911, "b1_1": 0.027795796031250652, "a2_0": 3308.274658619428, "a2_1": 0.16523236331162441, "b2_0": 367.9732263854306, "b2_1": 1.3317361363431022, "a3_0": 73.19056812685912, "a3_1": 0.0661688859750417, "b3_0": 2283.2554509507595, "b3_1": 0.3337501059568756, "bh_0": 0.9630015061711104, "bh_1": 4.335694369456647, "bh_2": 0.12228161756894262,"ah_0": 3.78837998891378, "ah_1": 10222.772037890725, "ah_2": 0.0343298286662707, "vShift": -20.438350564204057, "vShift_inact": 6.854888556940034, "maxrate": 11.69263400283082},
                # "unk4_garb":{"a1_0": 249.39394676887173, "a1_1": 0.5200041211792088, "b1_0": 3.0537485051086946, "b1_1": 0.011079128826530598, "a2_0": 6292.305271887281, "a2_1": 0.2262133494820389, "b2_0": 497.1694625984061, "b2_1": 2.8252370303536907, "a3_0": 120.78433837433904, "a3_1": 0.03591021839842313, "b3_0": 2270.1015688166062, "b3_1": 0.08572992894240089, "bh_0": 6.491149910777123, "bh_1": 17.665022890642007, "bh_2": 0.14407175708969008, "ah_0": 9.60984612337702, "ah_1": 532642.1308717187, "ah_2": 0.061140727260182305, "vShift": -13.706688544793083, "vShift_inact": 1.4432486979486674, "maxrate": 13.228182880636965},
                # "m109ttp8":{"a1_0": 20.738270571725597, "a1_1": 0.3886703764344085, "b1_0": 1.7777657212116993, "b1_1": 0.07133880391845333, "a2_0": 13738.752894030553, "a2_1": 0.001072434705231412, "b2_0": 316.67344931792195, "b2_1": 2.259989170117984, "a3_0": 244.7527462755213, "a3_1": 0.12579717339767021, "b3_0": 3128.4818314898152, "b3_1": 0.03983978451064088, "bh_0": 1.1794987814522668, "bh_1": 3.0406715641209985, "bh_2": 0.1386771747691053, "ah_0": 1.2034863037905796, "ah_1": 162725.3723019725, "ah_2": 0.06330126798417667, "vShift": -16.010025990356915, "vShift_inact": 5.31092545822662, "maxrate": 9.70064278311512},
                # "unk6_garb":{"a1_0": 95.70801317669665, "a1_1": 0.869609530944387, "b1_0": 3.011028429230476, "b1_1": 0.12148888744920948, "a2_0": 9467.538859037928, "a2_1": 0.05069924707277115, "b2_0": 328.70674342570953, "b2_1": 2.805835221891905, "a3_0": 236.46741316843074, "a3_1": 0.03888384499371427, "b3_0": 2742.8853120606755, "b3_1": 0.12424599531853064, "bh_0": 3.6883548795186276, "bh_1": 5.757168810270557, "bh_2": 0.1491082064678782, "ah_0": 0.49678697695149676, "ah_1": 19760.477056402495, "ah_2": 0.04503014445432112, "vShift": -25.144371628489367, "vShift_inact": 15.22740056713415, "maxrate": 314.18976984743983},
                # }               
                
                # changesna12 = {"m1012ttp8":{"a1_0": 62.774771313021546,"a1_1": 0.6854152336583206,"b1_0": 3.2117067311143277,"b1_1": 0.1432460480232296, "a2_0": 2468.966900014909,"a2_1": 0.0834387238328, "b2_0": 490.16060600231606,"b2_1": 2.969500725999265,"a3_0": 190.5883640336242,"a3_1": 0.003108395956123883,"b3_0": 7689.251014289831, "b3_1": 0.04054164070835632,"bh_0": 4.063594186259147,"bh_1": 2.115884898210715, "bh_2": 0.1433653421971472,"ah_0": 1.3563238605774417,"ah_1": 6568.351916792737, "ah_2": 0.011127551783912584,"vShift": -18.276678986708095, "vShift_inact": 16.74204011921361, "maxrate": 6.170113221706686}                
                # }        
                               
                ##Uncomment if want to update params file to update mod file!!!
                # nf.modify_dict_file(filename12, changesna12)
                # nf.modify_dict_file(filename16, changesna16)
                

                for mutname,dict in changesna12.items():
                        print(f"mutname is {mutname}")
                        print(f"it's corresponding dictionary is {dict}")
                        nf.modify_dict_file(filename12,dict)
                        nf.modify_dict_file(filename16,changesna16)


                
                ##TF042324 replace hmmWT with mut10_1 to account for different Tau0's in HH vs HMM vclamp act/inact/tau0 plots
                ##TF050724 Baseline params: ais_nav12_fac=1,ais_nav16_fac=1,nav12=2,nav16=7, somaK=1, KP=100, KT=1,ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,
                ##TF050824 putting in 1.6HMM 'na16mut44_092623' instead of na16HH_TF2 (HH 1.6)
                ##TF052424 Baseline 12HMM16HH params following bug fixes: ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=100, KT=1,ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1 
                        sim = tf.Na12Model_TF(ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=100, KT=1, 
                                        ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                        plots_folder = f'{root_path_out}/1-{mutname}', pfx=f'WT_', update=True)
                        
                        
                                        
                        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
                        plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                        fig_volts.savefig(f'{sim.plot_folder}/1-{mutname}.pdf')
                
                # sim.save2text(ais_nav12_fac=8,ais_nav16_fac=i16,nav12=1,nav16=15,
                #                 na12name = 'na12_HMM_TF100923-2',mut_name = 'na12_HMM_TF100923-2',na12mechs = ['na12annaTFHH','na12annaTFHH'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16HH_TF','na16HH_TF'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/gbar.01_1216-115_ais88_KP-{i12}----TEST')

                ##Plotting WT vs Mut Stim/DVDT/FI/Currentscapes
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                        sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'12-2.5_16-2.5_')#fnpre=f'{mutTXT}')
                # # # features_df = ef.get_features(sim=sim,mutTXT='WT_soma', mut_name = 'na12_HMM_TF100923')  
                
                        # sim.plot_fi_curve(start=0,end=2,nruns=21,wt_data = None,ax1 = None, fig = None,fn = 'ficurve')
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=100,stim_start=30, sweep_len=100)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=200,stim_start=30, sweep_len=200)
                
                        sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)
                        sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1075,stim_start=700, sweep_len=1200)
                
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
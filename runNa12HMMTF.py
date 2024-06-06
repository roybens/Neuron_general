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


root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/Restart030824/12-synthmuts_for_ramp'
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
                
                ##TF060324 WT params for WTvMUT comparison plots (black)
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
                # changesna12 = {
                # "m1012ttp8":{"a1_0": 62.774771313021546,"a1_1": 0.6854152336583206,"b1_0": 3.2117067311143277,"b1_1": 0.1432460480232296, "a2_0": 2468.966900014909,"a2_1": 0.0834387238328, "b2_0": 490.16060600231606,"b2_1": 2.969500725999265,"a3_0": 190.5883640336242,"a3_1": 0.003108395956123883,"b3_0": 7689.251014289831, "b3_1": 0.04054164070835632,"bh_0": 4.063594186259147,"bh_1": 2.115884898210715, "bh_2": 0.1433653421971472,"ah_0": 1.3563238605774417,"ah_1": 6568.351916792737, "ah_2": 0.011127551783912584,"vShift": -18.276678986708095, "vShift_inact": 16.74204011921361, "maxrate": 6.170113221706686},
                # "M1879T":{"a1_0": 171.65404967593912, "a1_1": 1.5473325780407043, "b1_0": 0.15668688284445786, "b1_1": 0.056578266862296, "a2_0": 10626.926411489329, "a2_1": 0.00041480337573633966, "b2_0": 29.048765867503395, "b2_1": 2.3342903358554383, "a3_0": 249.39252673373483, "a3_1": 0.0007503117414607886, "b3_0": 3066.9638504829777, "b3_1": 0.0188555817486158, "bh_0": 2.040068926358947, "bh_1": 3.7675241580162835, "bh_2": 0.02942144917704831, "ah_0": 0.4337041832768786, "ah_1": 6129.875372384539, "ah_2": 0.19871362195779174, "vShift": -16.853808606641802, "vShift_inact": 16.23871522904293, "maxrate": 147.56435592144186},
                # "F257I":{"a1_0": 57.23222656544356, "a1_1": 0.5162476539537184, "b1_0": 1.8724690877184815, "b1_1": 0.3489228884827919, "a2_0": 6511.174812425784, "a2_1": 0.31511083304771054, "b2_0": 13.931212257800585, "b2_1": 3.549602963154167, "a3_0": 56.06617645856018, "a3_1": 0.20253982835842732, "b3_0": 4557.794989159212, "b3_1": 0.10663558594679154, "bh_0": 7.710006832717681, "bh_1": 14.572356290822542, "bh_2": 0.18368832756574835, "ah_0": 13.135285500451904, "ah_1": 582694.8911257205, "ah_2": 0.02450775477624999, "vShift": -14.790198857295309, "vShift_inact": 2.5986463273723643, "maxrate": 5.6664026906358025},
                # "R1319G":{"a1_0": 11.725759655362136, "a1_1": 0.6571531403024519, "b1_0": 3.0065976174556512, "b1_1": 0.000902768010717224, "a2_0": 1742.7495829655707, "a2_1": 0.02251125633593753, "b2_0": 614.4646768407794, "b2_1": 0.8050557697779577, "a3_0": 15.468721657456264, "a3_1": 0.32793109120367053, "b3_0": 373.37385954192274, "b3_1": 0.05757001644645299, "bh_0": 2.2549687674388137, "bh_1": 6.916265330343567, "bh_2": 0.14921327138251256, "ah_0": 5.65060809152757, "ah_1": 45547.750321981424, "ah_2": 0.013818403982389392, "vShift": -19.406600254786213, "vShift_inact": 6.25935187673563, "maxrate": 8.684150279900209},
                # "K1480E":{"a1_0": 307.00465576071645, "a1_1": 0.49198920082186476, "b1_0": 5.4276811512377, "b1_1": 0.4969838847492478, "a2_0": 22407.406708905273, "a2_1": 0.06296552204807644, "b2_0": 563.8533209681815, "b2_1": 0.4087458667615537, "a3_0": 225.3447082584479, "a3_1": 0.07259909061390746, "b3_0": 1335.942117834803, "b3_1": 0.023939088443790713, "bh_0": 11.240863085795546, "bh_1": 3.944597572625594, "bh_2": 0.13803337916549033, "ah_0": 10.560716200998332, "ah_1": 27038.18935249356, "ah_2": 0.014812167953595981, "vShift": -9.845708608417436, "vShift_inact": 15.305677325325039, "maxrate": 7.30690132513435},
                # }

                # ##TF050824 mut10_5-13 fit to mut10_9_TTP8.
                # changesna12={"mut10_1":{"a1_0": 559.7395419475644, "a1_1": 1.6118947252237623, "b1_0": 5.796942895005852, "b1_1": 0.20673060819899028, "a2_0": 295.4715442119816, "a2_1": 0.12537078916956412, "b2_0": 430.8313126896239, "b2_1": 1.7648077505728925, "a3_0": 129.7287050319431, "a3_1": 0.0003735690025623176, "b3_0": 2352.673950047887, "b3_1": 0.0016281043181984676, "bh_0": 6.9512171030939225, "bh_1": 19.216471399067036, "bh_2": 0.14912604559884945, "ah_0": 5.31458071865826, "ah_1": 370404.9184628065, "ah_2": 0.033066372644917824, "vShift": -20.863377868930726, "vShift_inact": 7.165301442401468, "maxrate": 6.347893802473519},
                # "mut10_2":{"a1_0": 233.5849496343501, "a1_1": 1.1100362570504334, "b1_0": 5.817733516942724, "b1_1": 0.031198631197451615, "a2_0": 15143.165012586116, "a2_1": 0.5253983534312439, "b2_0": 354.8420877055062, "b2_1": 3.5709646528595798, "a3_0": 33.07985840619355, "a3_1": 0.27741220332436495, "b3_0": 2256.9955010874014, "b3_1": 0.05062650609669392, "bh_0": 9.165928629678628, "bh_1": 16.02677567882732, "bh_2": 0.14053201555721923, "ah_0": 0.5466576076284593, "ah_1": 6625.452699667287, "ah_2": 0.010092354464189518, "vShift": -20.158401170349244, "vShift_inact": 11.40838113481485, "maxrate": 5.205532628717714},
                # "mut10_5":{"a1_0": 0.8175962816429524, "a1_1": 0.03121588205834508, "b1_0": 0.0744746673948754, "b1_1": 0.11132158830492389, "a2_0": 13204.230002229458, "a2_1": 0.29183830413118095, "b2_0": 210.59427221114564, "b2_1": 3.0076977989068494, "a3_0": 433.53933597234834, "a3_1": 0.6042865823792669, "b3_0": 3694.1850011718543, "b3_1": 0.0043361248255975905, "bh_0": 5.138776755600741, "bh_1": 21.03421879541667, "bh_2": 0.1541931680140676, "ah_0": 4.895667727252144, "ah_1": 582713.9019979399, "ah_2": 0.040828796941040836, "vShift": -23.553779671048197, "vShift_inact": 5.959082612067263, "maxrate": 545.0549385972084},
                # "mut10_11":{"a1_0": 217.7764882719917, "a1_1": 1.2612334352408952, "b1_0": 0.5846218025336629, "b1_1": 0.13370425308851036, "a2_0": 3579.742201167344, "a2_1": 0.07315956734123634, "b2_0": 278.64110430289185, "b2_1": 2.5734484894546816, "a3_0": 67.88169140957082, "a3_1": 0.0023832979960251707, "b3_0": 1866.4702456069604, "b3_1": 0.008044061686699893, "bh_0": 14.065066558610647, "bh_1": 16.476536049649454, "bh_2": 0.1556431137159366, "ah_0": 7.810470437910962, "ah_1": 36495.04445494566, "ah_2": 0.012812791696751438, "vShift": -19.684977985113353, "vShift_inact": 9.35822463506868, "maxrate": 17.048642602049483},
                # "mut10_12":{"a1_0": 176.82754568537737, "a1_1": 1.1357123544748395, "b1_0": 2.716494618885052, "b1_1": 0.13496978675965182, "a2_0": 9644.440337089069, "a2_1": 0.2492458066485585, "b2_0": 327.19664715810313, "b2_1": 1.1440846054390899, "a3_0": 299.0379432813013, "a3_1": 0.12257136273310859, "b3_0": 1150.4174072857923, "b3_1": 0.08681076091384185, "bh_0": 8.375925558464942, "bh_1": 18.515986245733306, "bh_2": 0.1519784204033135, "ah_0": 47.30457040561784, "ah_1": 448381.62379709654, "ah_2": 0.016367957467689927, "vShift": -20.274284848494048, "vShift_inact": 6.641397859744719, "maxrate": 8.538014017714168},
                # "mut13_1":{"a1_0": 9.61468854373711, "a1_1": 0.63981735119507, "b1_0": 1.7708324593790925, "b1_1": 0.023252185072425338, "a2_0": 9086.760726813287, "a2_1": 0.04981931506718382, "b2_0": 517.5253863068335, "b2_1": 0.10061755767827041, "a3_0": 224.8874692275083, "a3_1": 0.001215260894700042, "b3_0": 3363.2649329253763, "b3_1": 0.0026626146982529925, "bh_0": 3.7683611073069807, "bh_1": 6.080192020592501, "bh_2": 0.1467600345973244, "ah_0": 14.108869399629521, "ah_1": 109128.48087846422, "ah_2": 0.016707452916454046, "vShift": -21.8070807327557, "vShift_inact": 11.453832052991128, "maxrate": 304.29965555183276},
                # "mut13_3":{"a1_0": 123.43590257466111, "a1_1": 0.9606706486679034, "b1_0": 1.6544526887443052, "b1_1": 0.5190803459628421, "a2_0": 8860.792503037395, "a2_1": 0.0259152951385715, "b2_0": 515.986001609208, "b2_1": 2.6720256115529626, "a3_0": 149.918074999944, "a3_1": 0.47244003927961853, "b3_0": 5760.358980957602, "b3_1": 0.003643199440391494, "bh_0": 2.7749126097624224, "bh_1": 10.477612485756303, "bh_2": 0.1425274562050642, "ah_0": 8.518223439905217, "ah_1": 61681.313529365114, "ah_2": 0.01879634480614487, "vShift": -19.514832178707998, "vShift_inact": 4.70034350103844, "maxrate": 3.653930459320725},
                # "mut2_1":{"a1_0": 33.69160414401048, "a1_1": 1.0409215382949943, "b1_0": 1.553890894354734, "b1_1": 0.4639646325911135, "a2_0": 833.6652202705059, "a2_1": 0.36213493264117974, "b2_0": 190.30475567949446, "b2_1": 6.6825415217044615, "a3_0": 60.75221805509284, "a3_1": 0.025256117763653566, "b3_0": 323.9549695047979, "b3_1": 0.0003950070087891779, "bh_0": 5.902835214676092, "bh_1": 14.706918666512493, "bh_2": 0.1647337851792094, "ah_0": 4.060160699409881, "ah_1": 332276.7106774799, "ah_2": 0.06852037308608006, "vShift": -23.823948323504787, "vShift_inact": 7.568979360707896, "maxrate": 4.45678670690157},
                # }            
                
                ##TF052224 WT for Het and KO experiments
                # changesna12 = {"m1012ttp8":{"a1_0": 62.774771313021546,"a1_1": 0.6854152336583206,"b1_0": 3.2117067311143277,"b1_1": 0.1432460480232296, "a2_0": 2468.966900014909,"a2_1": 0.0834387238328, "b2_0": 490.16060600231606,"b2_1": 2.969500725999265,"a3_0": 190.5883640336242,"a3_1": 0.003108395956123883,"b3_0": 7689.251014289831, "b3_1": 0.04054164070835632,"bh_0": 4.063594186259147,"bh_1": 2.115884898210715, "bh_2": 0.1433653421971472,"ah_0": 1.3563238605774417,"ah_1": 6568.351916792737, "ah_2": 0.011127551783912584,"vShift": -18.276678986708095, "vShift_inact": 16.74204011921361, "maxrate": 6.170113221706686}                
                # }        
                
                ##TF060324 Running Adil's mutants from a long time ago for manuscript fig (7 or something near the end)
                # changesna12 = {#"E1211K":{"a1_0": 7.435144546672603, "a1_1": NaN, "b1_0": 0.4348755059637439, "b1_1": 0.19474600087713761, "a2_0": 29433.11546477465, "a2_1": 0.03263511851664478, "b2_0": 230.2217338414771, "b2_1": 2.4979984850268067, "a3_0": 212.23732906199297, "a3_1": 0.013236134654001405, "b3_0": 1124.756935018952, "b3_1": 0.1462174775947988, "bh_0": 1.4055397630554942, "bh_1": 1.6636779195062226, "bh_2": 0.1078300176578646, "ah_0": 1.6714505194531035, "ah_1": 2063.76128431721, "ah_2": 0.007101866739255426, "vShift": -22.71793541492197, "vShift_inact": 17.54103368135606, "maxrate": 8924736.474769713},
                #                "K1422E":{"a1_0": 79.67927861712776, "a1_1": 0.7552503481209604, "b1_0": 1.966967744215963, "b1_1": 0.08864834507649852, "a2_0": 24962.148320424283, "a2_1": 0.014726475127559507, "b2_0": 455.40125772479365, "b2_1": 2.7266807397791255, "a3_0": 255.8273616636267, "a3_1": 0.16139904146552256, "b3_0": 1819.3100182914623, "b3_1": 0.16113096384894884, "bh_0": 3.9105109458354006, "bh_1": 9.155578731623088, "bh_2": 0.09903304010243566, "ah_0": 3.04819368655218, "ah_1": 111838.35151265633, "ah_2": 0.03495787709121393, "vShift": -14.24090286900306, "vShift_inact": 15.74901123757051, "maxrate": 106.14963123802909},
                #                "R379H":{"a1_0": 4.218414685978145, "a1_1": 0.07752734254016345, "b1_0": 3.5671677351352535, "b1_1": 0.08928217476900027, "a2_0": 6292.73308654195, "a2_1": 0.015238482597440317, "b2_0": 433.5311800226415, "b2_1": 3.0174743142166407, "a3_0": 270.9643098259681, "a3_1": 0.0467051311630961, "b3_0": 1842.510959416778, "b3_1": 0.0851944301558436, "bh_0": 10.29264652331339, "bh_1": 10.0, "bh_2": 0.15486677311263308, "ah_0": 0.09236383526611308, "ah_1": 118930.65573333694, "ah_2": 0.07625692582735874, "vShift": -22.644611110587487, "vShift_inact": 18.315001126016156, "maxrate": 437522225.47954637},
                #                "R853Q":{"a1_0": 320.0000061911132, "a1_1": 0.1797343516281184, "b1_0": 3.0412107502325374, "b1_1": 0.06337431243687862, "a2_0": 9425.519440296275, "a2_1": 0.05806193504134175, "b2_0": 369.25315117977493, "b2_1": 3.255451078701526, "a3_0": 277.0946787549736, "a3_1": 0.8441329470092859, "b3_0": 2480.695688197943, "b3_1": 0.12850930360605184, "bh_0": 8.949838946050704, "bh_1": 3.915582806793515, "bh_2": 0.1491082064678782, "ah_0": 0.8902261110327658, "ah_1": 50823.04384183572, "ah_2": 0.04559563914112795, "vShift": -22.218080220188746, "vShift_inact": 5.770135836736812, "maxrate": 1760.4067010351296},
                #                "R937C":{"a1_0": 4.644433794651973, "a1_1": 0.060229725282229585, "b1_0": 4.752575388604706, "b1_1": 0.0017400907600393298, "a2_0": 1952.9053448706927, "a2_1": 0.30261277680277765, "b2_0": 381.19400526802224, "b2_1": 1.529922263969305, "a3_0": 312.5969670043847, "a3_1": 0.0006164818726001932, "b3_0": 2389.862026365366, "b3_1": 0.1362779137987642, "bh_0": 6.40717556426052, "bh_1": 7.174840649081506, "bh_2": 0.1525760923986528, "ah_0": 1.0254610289394637, "ah_1": 53551.004499141156, "ah_2": 0.05325668023299314, "vShift": -22.363522600475736, "vShift_inact": 17.085816515345602, "maxrate": 73729580.21057054},
                #                "T400R":{"a1_0": 258.62803333363286, "a1_1": 0.9099717140716234, "b1_0": 3.4851938622474607, "b1_1": 0.0072834304514034776, "a2_0": 8699.467838160175, "a2_1": 0.0658754833376706, "b2_0": 427.68748281548244, "b2_1": 2.0615045331667745, "a3_0": 230.624639093987, "a3_1": 0.019235152474900388, "b3_0": 1447.3579918868552, "b3_1": 0.09992578324519744, "bh_0": 4.720669331101204, "bh_1": 1.8308553442641797, "bh_2": 0.1231626533860089, "ah_0": 1.6573544890880583, "ah_1": 22720.004616919294, "ah_2": 0.03265772985301202, "vShift": -24.092498849608997, "vShift_inact": 18.57301697165515, "maxrate": 1648.4107234876903}
                #                }
                
                ##TF060424 Synth muts to see if we can improve ramp and het/KO behavior
                # changesna12 ={"mut2_1":{"a1_0": 69.12757487649847, "a1_1": 0.789767815912694, "b1_0": 3.4643953815306943, "b1_1": 0.1611806334303184, "a2_0": 17103.27339572192, "a2_1": 0.11243773096831099, "b2_0": 476.72877060400054, "b2_1": 1.0209048241624212, "a3_0": 139.89532268858247, "a3_1": 0.12883874864472844, "b3_0": 5406.6580871179485, "b3_1": 0.04835725599687075, "bh_0": 5.944563305275702, "bh_1": 6.11870416906392, "bh_2": 0.1630316734399037, "ah_0": 1.0146684531626238, "ah_1": 443254.22005664255, "ah_2": 0.0689195977492152, "vShift": -21.221303362372442, "vShift_inact": 9.95800959842116, "maxrate": 5.5161094749427235},
                #         "mut2_4":{"a1_0": 1.3866064393534998, "a1_1": 0.545145585352073, "b1_0": 1.8020161314907286, "b1_1": 0.046627091112890554, "a2_0": 5789.312942185273, "a2_1": 0.034871001525536544, "b2_0": 549.835788492507, "b2_1": 3.8623034672604666, "a3_0": 231.4635697668745, "a3_1": 0.006026029944200411, "b3_0": 2391.9843119415455, "b3_1": 0.03840126649745168, "bh_0": 3.2225223772548484, "bh_1": 10.54256918269265, "bh_2": 0.14120713839760488, "ah_0": 0.9209252908336144, "ah_1": 80184.12281248448, "ah_2": 3.036081615601853e-05, "vShift": -17.393200425252374, "vShift_inact": 4.826247509532424, "maxrate": 4024.1332603103624},
                #         #Nan# "mut3_1":{"a1_0": 86.20279670360574, "a1_1": 0.4807157759772428, "b1_0": 1.0418431121333143, "b1_1": 0.15955947869235565, "a2_0": 8117.846228009379, "a2_1": 0.22905299593179226, "b2_0": 579.2881452762555, "b2_1": 4.167792757117611, "a3_0": 323.4918853926455, "a3_1": 0.5313228051428169, "b3_0": 1729.166118699934, "b3_1": 0.08317046355865362, "bh_0": 6.772300895664214, "bh_1": 22.643018511341197, "bh_2": 0.14302541140436442, "ah_0": 4.149616517565889, "ah_1": 89246.43408047478, "ah_2": NaN, "vShift": -16.86496095261703, "vShift_inact": 3.0600220976340644, "maxrate": 5.147002319337144},
                #         "mut3_4":{"a1_0": 128.53591097170286, "a1_1": 1.0088810605081322, "b1_0": 2.8057181138811145, "b1_1": 0.2022861070881682, "a2_0": 24235.28384053261, "a2_1": 0.4671683117086187, "b2_0": 91.69289962895067, "b2_1": 1.0654933675687197, "a3_0": 26.50431843916422, "a3_1": 0.11887201238816543, "b3_0": 8306.767588743529, "b3_1": 0.005820187365139326, "bh_0": 9.448415384697004, "bh_1": 8.275246581573324, "bh_2": 0.14413346182855655, "ah_0": 4.7838628466405275, "ah_1": 72796.02218145091, "ah_2": 0.013572592312347621, "vShift": -19.864102343296103, "vShift_inact": 15.107014626332832, "maxrate": 5.565964757674081},
                #         "mut4_1":{"a1_0": 6.629520609118986, "a1_1": 0.5339177792056462, "b1_0": 1.4360470073080234, "b1_1": 0.10184737858925721, "a2_0": 7788.203978066607, "a2_1": 0.08393027619983062, "b2_0": 756.032865539491, "b2_1": 3.1680485738626554, "a3_0": 128.38893986990055, "a3_1": 9.153035478613465e-05, "b3_0": 1177.239191690016, "b3_1": 0.1745137786840211, "bh_0": 10.409954196682733, "bh_1": 4.446711842865597, "bh_2": 0.11007283099488524, "ah_0": 1.7428955764725829, "ah_1": 2255.5755057905553, "ah_2": 0.0014383952348937853, "vShift": -20.27742168046784, "vShift_inact": 22.61957308104258, "maxrate": 6.477205703437239},
                #         "mut4_4":{"a1_0": 66.55295107486042, "a1_1": 1.0157222683008331, "b1_0": 2.443727704461094, "b1_1": 0.14756130074098994, "a2_0": 8413.475464739966, "a2_1": 0.052763530701047785, "b2_0": 254.22156882892654, "b2_1": 2.502925986518344, "a3_0": 281.0770245709674, "a3_1": 0.09810778836534739, "b3_0": 2111.1517558836617, "b3_1": 0.020887193118835284, "bh_0": 6.079283862575461, "bh_1": 7.31652673186878, "bh_2": 0.30503956445995517, "ah_0": 6.4256441034248315, "ah_1": 328495.54784845683, "ah_2": 0.06523036884022816, "vShift": -18.63763619779751, "vShift_inact": 0.18750870355926752, "maxrate": 8.940366254600413},
                #         #Nan# "mut10_1":{"a1_0": 191.43519559307776, "a1_1": 0.7461828329339152, "b1_0": 5.765351641337009, "b1_1": 0.08913421188641882, "a2_0": 1058.1289903802947, "a2_1": 0.0008746088404807863, "b2_0": 473.91180554758006, "b2_1": 2.012367668844246, "a3_0": 27.99487518679058, "a3_1": 0.12022871615904279, "b3_0": 8989.354166603882, "b3_1": 0.052164005276735356, "bh_0": 8.220513752960091, "bh_1": 14.008534092096573, "bh_2": 0.15094181409183854, "ah_0": 10.193271866842117, "ah_1": 1017219.1807581247, "ah_2": NaN, "vShift": -17.963408474754168, "vShift_inact": 7.143422121793371, "maxrate": 6.397028280745049},
                #         "mut10_4":{"a1_0": 30.990568607464937, "a1_1": 0.727207131085451, "b1_0": 2.4177659248112304, "b1_1": 0.001361137402837942, "a2_0": 7764.878961142766, "a2_1": 0.033710133967452593, "b2_0": 354.5075793923026, "b2_1": 4.0585190172293055, "a3_0": 124.65125337416927, "a3_1": 0.002466385979914096, "b3_0": 5691.006145002193, "b3_1": 0.0062791739575876, "bh_0": 0.7148812999656258, "bh_1": 1.0205850850329137, "bh_2": 0.1491648507752708, "ah_0": 11.231511989775173, "ah_1": 29046.460566891234, "ah_2": 0.008490668279800669, "vShift": -19.00612418597558, "vShift_inact": 8.677200690072695, "maxrate": 5.262143195447436},
                #         #Nan# "mut11_1":{"a1_0": 145.48905209314754, "a1_1": 1.593365639673773, "b1_0": 3.5305851826156553, "b1_1": 0.0005968644547289601, "a2_0": 12118.243166837574, "a2_1": 0.10615706172381738, "b2_0": 265.847828270064, "b2_1": 1.5667825243211015, "a3_0": 32.20936934781723, "a3_1": 0.0016520123483112284, "b3_0": 3432.6915138541326, "b3_1": 0.07184995204741153, "bh_0": 3.3588452066360315, "bh_1": 6.8515702831176934, "bh_2": 0.14187764262354707, "ah_0": NaN, "ah_1": 7647.049372709804, "ah_2": 0.0049997089876087815, "vShift": -21.501764494610228, "vShift_inact": 10.499505063822248, "maxrate": 9.756910522888205},
                #         #Nan# "mut11_4":{"a1_0": 6.938855908417205, "a1_1": 0.7891228369673836, "b1_0": 4.561719983300476, "b1_1": 0.1659089912713404, "a2_0": 16902.834045540385, "a2_1": 0.022023411266043097, "b2_0": 590.2820732089813, "b2_1": 0.840735279873617, "a3_0": 143.96184790691095, "a3_1": 0.3027875941586524, "b3_0": 6570.9105638396395, "b3_1": 0.025507972097138273, "bh_0": 3.811470101806895, "bh_1": 21.246182313226768, "bh_2": 0.1419108995771584, "ah_0": NaN, "ah_1": 1134136.8671543072, "ah_2": 0.0539527302001787, "vShift": -21.7750606223955, "vShift_inact": 5.226866419408855, "maxrate": 7.1565185367798065},
                #         "mut11_5":{"a1_0": 97.02872326135682, "a1_1": 0.8386780186065939, "b1_0": 4.156105827893548, "b1_1": 0.08855380365761789, "a2_0": 22686.355262865098, "a2_1": 0.14012414859610794, "b2_0": 123.72078902474202, "b2_1": 7.571812884512333, "a3_0": 212.45109352018738, "a3_1": 0.01920111561645514, "b3_0": 5153.35576218601, "b3_1": 0.00414632428617805, "bh_0": 5.939474156048486, "bh_1": 28.460828634562287, "bh_2": 0.14582883646047484, "ah_0": 6.070809736302203, "ah_1": 109875.04982107758, "ah_2": 0.025060371247176624, "vShift": -18.682713628750207, "vShift_inact": 1.6282364265890426, "maxrate": 5.574859402644158},
                #         #Nan# "mut11_6":{"a1_0": 7.77746305119928, "a1_1": 0.6151424904143152, "b1_0": 4.250639827299032, "b1_1": 0.12230358031547345, "a2_0": 14385.710148596936, "a2_1": 0.08711984823065401, "b2_0": 193.82725476583778, "b2_1": 2.574813302796789, "a3_0": 175.18825127321674, "a3_1": 0.07169758934618597, "b3_0": 5233.866864783647, "b3_1": 0.03889123855779479, "bh_0": 3.2822632550879707, "bh_1": 11.988513444941484, "bh_2": 0.14060940235600006, "ah_0": NaN, "ah_1": 4138.320883103981, "ah_2": 0.00047285266293792803, "vShift": -20.714904507995332, "vShift_inact": 4.6723982856856745, "maxrate": 6.020055530461606},
                #         #Nan# "mut11_7":{"a1_0": 28.3106951014515, "a1_1": 0.5612567010821508, "b1_0": 4.85439749127157, "b1_1": 0.023555247103909556, "a2_0": 6735.167351229368, "a2_1": 0.07056313336643306, "b2_0": 737.109338145104, "b2_1": 1.9625821948635076, "a3_0": 161.77350522544967, "a3_1": 0.07928248927733096, "b3_0": 4121.372440642053, "b3_1": 0.024403762888971822, "bh_0": 8.406227505668394, "bh_1": 22.965592956534994, "bh_2": 0.14805798481398397, "ah_0": NaN, "ah_1": 201928.04174326546, "ah_2": 0.02526866811390316, "vShift": -17.996264525883028, "vShift_inact": 4.634802954746487, "maxrate": 8.67870002479815},
                #         #Nan# "mut11_8":{"a1_0": 3.934077594718162, "a1_1": 0.41864010446977684, "b1_0": 2.7930158882330254, "b1_1": 0.0026521945511908396, "a2_0": 759.2062572566573, "a2_1": 0.4140784248143825, "b2_0": 217.5275692215929, "b2_1": 1.007681377881737, "a3_0": 42.36786354405925, "a3_1": 0.2971779569314839, "b3_0": 4046.212380341188, "b3_1": 0.03743338109037109, "bh_0": 3.7721925434904326, "bh_1": 27.123936635333738, "bh_2": 0.14825020327545935, "ah_0": NaN, "ah_1": 605270.0829383364, "ah_2": 0.053098167494161214, "vShift": -20.118579344941335, "vShift_inact": 0.36005298736157887, "maxrate": 6.068259036299933},
                #         #Nan# "mut11_9":{"a1_0": 141.9849501275761, "a1_1": 1.1085755202068512, "b1_0": 6.322653498055551, "b1_1": 0.015386207878437808, "a2_0": 9680.17876386771, "a2_1": 0.07979740589061102, "b2_0": 137.5447625950569, "b2_1": 1.9413582544833146, "a3_0": 87.08487239842628, "a3_1": 0.0040915161584304804, "b3_0": 9608.582703132137, "b3_1": 0.03494969491802795, "bh_0": 8.396181966678954, "bh_1": 29.355160806431307, "bh_2": 0.1453241430294208, "ah_0": NaN, "ah_1": 464889.9106152553, "ah_2": 0.0430218198508133, "vShift": -20.11993371049176, "vShift_inact": 5.657045961832672, "maxrate": 6.91128564013095},
                #         }
                
                changesna12={"mut10_4":{"a1_0": 30.990568607464937, "a1_1": 0.727207131085451, "b1_0": 2.4177659248112304, "b1_1": 0.001361137402837942, "a2_0": 7764.878961142766, "a2_1": 0.033710133967452593, "b2_0": 354.5075793923026, "b2_1": 4.0585190172293055, "a3_0": 124.65125337416927, "a3_1": 0.002466385979914096, "b3_0": 5691.006145002193, "b3_1": 0.0062791739575876, "bh_0": 0.7148812999656258, "bh_1": 1.0205850850329137, "bh_2": 0.1491648507752708, "ah_0": 11.231511989775173, "ah_1": 29046.460566891234, "ah_2": 0.008490668279800669, "vShift": -19.00612418597558, "vShift_inact": 8.677200690072695, "maxrate": 5.262143195447436}}
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
                ##TF052824 Testing different percentage KOs of 12HMM16HH model        
                        sim = tf.Na12Model_TF(ais_nav12_fac=0,ais_nav16_fac=7,nav12=0,nav16=2.5, somaK=1, KP=100, KT=1, #ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=100, KT=1, 
                                        ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                        plots_folder = f'{root_path_out}/2-{mutname}_KO', pfx=f'WT_', update=True)
                        
                        
                                        
                        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
                        plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                        fig_volts.savefig(f'{sim.plot_folder}/2-{mutname}_KO.pdf')
                
                # sim.save2text(ais_nav12_fac=8,ais_nav16_fac=i16,nav12=1,nav16=15,
                #                 na12name = 'na12_HMM_TF100923-2',mut_name = 'na12_HMM_TF100923-2',na12mechs = ['na12annaTFHH','na12annaTFHH'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16HH_TF','na16HH_TF'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/gbar.01_1216-115_ais88_KP-{i12}----TEST')

                ##Plotting WT vs Mut Stim/DVDT/FI/Currentscapes
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                        sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'het50')#fnpre=f'{mutTXT}')
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
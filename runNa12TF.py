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


root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/Restart030824/7-HH_plots_for_grants'

if not os.path.exists(root_path_out):
        os.makedirs(root_path_out)
        # os.mkdir(root_path_out)


vals =[1]#[1]#[-80,-70-60,-50,-40,-30]
vals2 = [1]#[-30,-40,-50,-60,-70,-80]#[1]

# for i12 in np.arange(1,6,1):     
        # for i16 in np.arange(10,50,10):
for i12 in vals:
        for i16 in vals2:
                ##Adding below function to loop through different na16.mod params        
                # filename = "/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TF100923-2.txt" ##TF031524 for changing 8st na12
                filename12 = '/global/homes/t/tfenton/Neuron_general-2/params/na12annaTFHH2.txt'
                filename16 = '/global/homes/t/tfenton/Neuron_general-2/params/na16HH_TF2.txt'

                ##1.2HH model
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
                
           
                # #16HH
                # changesna16 = {
                #         "sh": 8,
                #         "gbar": 0.01,
                #         "tha": -40, #noshift=-40,
                #         "qa": 7.2,
                #         "Ra": 0.4,
                #         "Rb": 0.124,
                #         "thi1": -30,#noshift=-30,
                #         "thi2": -30,#noshift=-30,
                #         "qd": 0.5,
                #         "qg": 1.5,
                #         "mmin": 0.02,  
                #         "hmin": 0.01,  
                #         "q10": 2,
                #         "Rg": 0.01,
                #         "Rd": 0.03,
                #         "thinf": -65,#noshift=-65,
                #         "qinf": 7,
                #         "vhalfs": -40,
                #         "a0s": 0.0003,
                #         "gms": 0.2,
                #         "zetas": 12,
                #         "smax": 10,
                #         "vvh": -58,
                #         "vvs": 2,
                #         "ar2": 1,
                #         #"ena": 55
                #         }
                
                ##TF051024 same params as in mod file na12annaTFHH.mod
                # changesna12 = {
                #         "sh": 8,#-3#i12,#8,
                #         "gbar": 0.0486,#0.245989,#0.01,#0.06,#0.1,#0.01,0.0486
                #         "tha": -38,#i12,#-38,
                #         "qa": 5.41,
                #         "Ra": 0.3282,
                #         "Rb": 0.1,
                #         "thi1": -80,#-80,
                #         "thi2": -80,#-80,
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
                # ##TF051024 same params as in mod file na16HH_TF.mod             
                # changesna16 = {
                #         "sh": 8,
                #         "gbar": 0.0394,#0.245989,#0.01,0.0486
                #         "tha": -47, #noshift=-40,
                #         "qa": 7.2,
                #         "Ra": 0.4,
                #         "Rb": 0.124,
                #         "thi1": -61,#noshift=-30,
                #         "thi2": -61,#noshift=-30,
                #         "qd": 0.5,
                #         "qg": 1.5,
                #         "mmin": 0.02,  
                #         "hmin": 0.01,  
                #         "q10": 2,
                #         "Rg": 0.01,
                #         "Rd": 0.03,
                #         "thinf": -65,#noshift=-65,
                #         "qinf": 7,
                #         "vhalfs": -40,
                #         "a0s": 0.0003,
                #         "gms": 0.2,
                #         "zetas": 12,
                #         "smax": 10,
                #         "vvh": -58,
                #         "vvs": 2,
                #         "ar2": 1,
                #         #"ena": 55
                #         }
                
                # nf.modify_dict_file(filename12, changesna12)
                # nf.modify_dict_file(filename16, changesna16)

                # for mutname,dict in changesna12.items():
                #         print(f"mutname is {mutname}")
                #         print(f"it's corresponding dictionary is {dict}")
                #         nf.modify_dict_file(filename12,dict)
                        # nf.modify_dict_file(filename16,changesna16)

                #################### HH MODEL ####################
                ##TF031924 These are the parameters that work best for 12HH16HH model!!!
                ##TF040224 Newly found best HH params following debugging of na12/16 and ais12/16 updating
                sim = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=2,nav12=3,nav16=1, somaK=1, KP=100, KT=10, #somaK=10 KP=20, KP=90_KT=40
                                        ais_ca = 1,ais_Kca = 1,soma_na16=1,soma_na12 = 1,node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40,
                                na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                                plots_folder = f'{root_path_out}/5_hcmd-ON_UMFD-OFF', pfx=f'WT_', update=True)
                #################### HH MODEL ####################
                
                
                
                
                                
                # fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
                # sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
                # plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
                # fig_volts.savefig(f'{sim.plot_folder}/5_hcmd-ON_UMFD-OFF.pdf')
                
                # sim.save2text(ais_nav12_fac=8,ais_nav16_fac=i16,nav12=1,nav16=15,
                #                 na12name = 'na12_HMM_TF100923-2',mut_name = 'na12_HMM_TF100923-2',na12mechs = ['na12annaTFHH','na12annaTFHH'],
                #                 na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16HH_TF','na16HH_TF'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/gbar.01_1216-115_ais88_KP-{i12}----TEST')

                ##Plotting WT vs Mut Stim/DVDT/FI/Currentscapes
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
                # sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'12-{i12}_16-{i16}_')#fnpre=f'{mutTXT}')
                # # # features_df = ef.get_features(sim=sim,mutTXT='WT_soma', mut_name = 'na12_HMM_TF100923')  
                
                # sim.plot_fi_curve(start=0,end=2,nruns=21,wt_data = None,ax1 = None, fig = None,fn = 'ficurve')
                sim.make_currentscape_plot(amp=0.5, time1=30,time2=50,stim_start=30, sweep_len=100)
                sim.make_currentscape_plot(amp=0.5, time1=30,time2=70,stim_start=30, sweep_len=100)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=200,stim_start=30, sweep_len=200)
                # sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)
                # sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1075,stim_start=700, sweep_len=1200)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=1200,stim_start=700, sweep_len=1200)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=500,stim_start=500, sweep_len=1000)
                # sim.make_currentscape_plot(amp=0.5, time1=0,time2=500,stim_start=600, sweep_len=1000)
                # sim.make_currentscape_plot(amp=0.5, time1=860,time2=890,stim_start=700, sweep_len=1000) #single AP




        
                #Make WT and save data for comparison later
                # sim = tf.Na12Model_TF(ais_nav12_fac=7,ais_nav16_fac = 7,nav12=4,nav16=3,somaK=i,na12name = 'na12_HMM_TF100923',mut_name = 'na12_HMM_TF100923',
                #                 na16mechs=['na16HH_TF','na16HH_TF'],params_folder = './params/na12HMM_allsynthmuts_HOFs/',
                #                 plots_folder = f'{root_path_out}/somaK-{i}', pfx=f'WT_')
                

                              
                
                


                
                ##TF040324 Different insufficiency experiments (50% het and 0% KO) HH model Het 50% and KO na12 everywhere (including ais)
                # simwt = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=2,nav12=3,nav16=1, somaK=1, KP=100, KT=10, #somaK=10 KP=20, KP=90_KT=40
                #                         ais_ca = 1,ais_Kca=1,soma_na16=1,soma_na12=1,node_na=1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40,
                #                         na12name = 'na12annaTFHH2',mut_name = 'na12annaTFHH2',na12mechs = ['na12','na12mut'],
                #                         na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                         plots_folder = f'{root_path_out}/2_KO_na12', pfx=f'WT_', update=True)
                # wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)

                   




                ##TF042324 replace hmmWT with mut10_1 to account for different Tau0's in HH vs HMM vclamp act/inact/tau0 plots
                ##TF050724 Baseline params: ais_nav12_fac=1,ais_nav16_fac=1,nav12=2,nav16=7, somaK=1, KP=100, KT=1,ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,
                ##TF050824 putting in 1.6HMM 'na16mut44_092623' instead of na16HH_TF2 (HH 1.6)
                # sim = tf.Na12Model_TF(ais_nav12_fac=1,ais_nav16_fac=1,nav12=i12,nav16=i16, somaK=1, KP=100, KT=1, #somaK=10  KP=14,100 KT=40, ais_nav12_fac=1.5,ais_nav16_fac=1.5,nav12=1,nav16=8, nav1216=2;5-10=1,7, 12=2 16=0.5
                #                 ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                #                 na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                #                 na16name = 'na16mut44_092623',na16mut_name = 'na16mut44_092623',na16mechs=['na16','na16mut'],params_folder = './params/',
                #                 plots_folder = f'{root_path_out}/3-mut109tt8-16HMM_1216_{i12}-{i16}', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}     









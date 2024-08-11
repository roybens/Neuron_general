
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
#import Document as doc
import Tim_ng_functions as nf




sim_config_soma = {
                'section' : 'soma',
                'segment' : 0.5,
                'section_num': 0,
                'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'], 
                'current_names' : ['Ih','SKv3_1','Na16 WT','Na16 WT','Na12','Na12 MUT','pas'],
                'ionic_concentrations' :["cai", "ki", "nai"]
    
                }


root_path_out = './Plots/GY_R850P_2024/Na12HMM16HH/R850P_062724/'


if not os.path.exists(root_path_out):
        os.makedirs(root_path_out)
        os.makedirs(root_path_out + '/3-WT')



#Dummy text files, the params will be replaced by what you give them when using nf.modify_dict_file
filename12 = './params/na12_HMM_TEMP_PARAMS.txt'
filename16 = './params/na16HH_TF2.txt'

                
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
                

                
             ##TF060324 (same as na12_HMM_TF050724) WT params for WTvMUT comparison plots (black)
changesna12a = {"a1_0": 62.774771313021546,"a1_1": 0.6854152336583206,"b1_0": 3.2117067311143277,"b1_1": 0.1432460480232296, "a2_0": 2468.966900014909,"a2_1": 0.0834387238328, "b2_0": 490.16060600231606,"b2_1": 2.969500725999265,"a3_0": 190.5883640336242,"a3_1": 0.003108395956123883,"b3_0": 7689.251014289831, "b3_1": 0.04054164070835632,"bh_0": 4.063594186259147,"bh_1": 2.115884898210715, "bh_2": 0.1433653421971472,"ah_0": 1.3563238605774417,"ah_1": 6568.351916792737, "ah_2": 0.011127551783912584,"vShift": -18.276678986708095, "vShift_inact": 16.74204011921361, "maxrate": 6.170113221706686}                
nf.modify_dict_file(filename12, changesna12a)
nf.modify_dict_file(filename16, changesna16)

simwt = tf.Na12Model_TF(ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=100, KT=1, 
                ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,
                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],params_folder = './params/',
                plots_folder = f'{root_path_out}/3-WT', pfx=f'WT_', update=True)

        
wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)             

 #plotting the WT
simwt.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)
simwt.make_currentscape_plot(amp=0.5, time1=1000,time2=1075,stim_start=700, sweep_len=1200)             

"""
##For mature model
changesna12 = {"R850P_062724_2000": {'a1_0': 41.24466597259794, 'a1_1': 0.5308501317510134, 'b1_0': 7.386920140708283, 'b1_1': 0.008256767752317935, 'a2_0': 10755.581571569404, 'a2_1': 0.2941534968877462, 'b2_0': 508.5221717496915, 'b2_1': 0.8344607280938177, 'a3_0': 357.34870015416504, 'a3_1': 0.0002195891536895594, 'b3_0': 1070.0986194771494, 'b3_1': 0.027183145081577945, 'bh_0': 3.7310446112469187, 'bh_1': 11.870394633074387, 'bh_2': 0.11998196950856949, 'ah_0': 11.265619816992157, 'ah_1': 711379.2077178769, 'ah_2': 0.0020378247251452777, 'vShift': -9.743154184024819, 'vShift_inact': 0.4138496607777782, 'maxrate': 10.159989993015305}}
    #"R850P_062624": {'a1_0': 41.24466597259794, 'a1_1': 0.5308501317510134, 'b1_0': 7.386920140708283, 'b1_1': 0.008256767752317935, 'a2_0': 10755.581571569404, 'a2_1': 0.2941534968877462, 'b2_0': 508.5221717496915, 'b2_1': 0.8344607280938177, 'a3_0': 357.34870015416504, 'a3_1': 0.0002195891536895594, 'b3_0': 1070.0986194771494, 'b3_1': 0.027183145081577945, 'bh_0': 3.7310446112469187, 'bh_1': 11.870394633074387, 'bh_2': 0.11998196950856949, 'ah_0': 11.265619816992157, 'ah_1': 711379.2077178769, 'ah_2': 0.0020378247251452777, 'vShift': -9.743154184024819, 'vShift_inact': 0.4138496607777782, 'maxrate': 10.159989993015305}}
                
#changesna12 = {"M1879T":{"a1_0": 171.65404967593912, "a1_1": 1.5473325780407043, "b1_0": 0.15668688284445786, "b1_1": 0.056578266862296, "a2_0": 10626.926411489329, "a2_1": 0.00041480337573633966, "b2_0": 29.048765867503395, "b2_1": 2.3342903358554383, "a3_0": 249.39252673373483, "a3_1": 0.0007503117414607886, "b3_0": 3066.9638504829777, "b3_1": 0.0188555817486158, "bh_0": 2.040068926358947, "bh_1": 3.7675241580162835, "bh_2": 0.02942144917704831, "ah_0": 0.4337041832768786, "ah_1": 6129.875372384539, "ah_2": 0.19871362195779174, "vShift": -16.853808606641802, "vShift_inact": 16.23871522904293, "maxrate": 147.56435592144186}}

for mutname,dict in changesna12.items():
    #for one mut: still use this for loop beacuse the mutname is being used
    print(f"mutname is {mutname}")
    print(f"it's corresponding dictionary is {dict}")
    nf.modify_dict_file(filengame12,dict)
    nf.modify_dict_file(filename16,changesna16)


    sim = tf.Na12Model_TF(ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=100, KT=1,  
                  ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,
                  na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                  na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],
                  params_folder = './params/',plots_folder = f'{root_path_out}/1-{mutname}', pfx=f'WT_', update=True)
                        
                        
                                        
    fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
    sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
    plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
    fig_volts.savefig(f'{sim.plot_folder}/1-{mutname}.pdf')

    sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KO')
    sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)
    sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1075,stim_start=700, sweep_len=1200)
    
    """
"""    
    
    
#For developing model
# For developing model we have two types, either replacing both Na16 alleles with Na12 WT or Na12Na12 Mut
changesna12 = {"R850P_062724_2000": {'a1_0': 41.24466597259794, 'a1_1': 0.5308501317510134, 'b1_0': 7.386920140708283, 'b1_1': 0.008256767752317935, 'a2_0': 10755.581571569404, 'a2_1': 0.2941534968877462, 'b2_0': 508.5221717496915, 'b2_1': 0.8344607280938177, 'a3_0': 357.34870015416504, 'a3_1': 0.0002195891536895594, 'b3_0': 1070.0986194771494, 'b3_1': 0.027183145081577945, 'bh_0': 3.7310446112469187, 'bh_1': 11.870394633074387, 'bh_2': 0.11998196950856949, 'ah_0': 11.265619816992157, 'ah_1': 711379.2077178769, 'ah_2': 0.0020378247251452777, 'vShift': -9.743154184024819, 'vShift_inact': 0.4138496607777782, 'maxrate': 10.159989993015305},
    "R850P_062624": {'a1_0': 41.24466597259794, 'a1_1': 0.5308501317510134, 'b1_0': 7.386920140708283, 'b1_1': 0.008256767752317935, 'a2_0': 10755.581571569404, 'a2_1': 0.2941534968877462, 'b2_0': 508.5221717496915, 'b2_1': 0.8344607280938177, 'a3_0': 357.34870015416504, 'a3_1': 0.0002195891536895594, 'b3_0': 1070.0986194771494, 'b3_1': 0.027183145081577945, 'bh_0': 3.7310446112469187, 'bh_1': 11.870394633074387, 'bh_2': 0.11998196950856949, 'ah_0': 11.265619816992157, 'ah_1': 711379.2077178769, 'ah_2': 0.0020378247251452777, 'vShift': -9.743154184024819, 'vShift_inact': 0.4138496607777782, 'maxrate': 10.159989993015305}}}}




#Na16 replaced with Na12WT
for mutname,dict in changesna12.items():
    #for one mut: still use this for loop beacuse the mutname is being used
    print(f"mutname is {mutname}")
    print(f"it's corresponding dictionary is {dict}")
    nf.modify_dict_file(filename12,dict)
    nf.modify_dict_file(filename16,changesna12)


    sim = tf.Na12Model_TF(ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=100, KT=1,  
                  ais_ca = 1,ais_Kca = 1, soma_na12=1, soma_na16=1, dend_nav12=1, node_na = 1,
                  na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                  na16name = 'na16HH_TF2',na16mut_name = 'na16HH_TF2',na16mechs=['na16','na16mut'],
                  params_folder = './params/',plots_folder = f'{root_path_out}/Developing_hom-{mutname}', pfx=f'WT_', update=True)
                        
                        
                                        
    fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
    sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
    plot_dvdt_from_volts(sim.volt_soma, sim.dt, axs[1],clr='cadetblue')
    fig_volts.savefig(f'{sim.plot_folder}/Developing_hom-{mutname}.pdf')

    sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KO')
    sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1200,stim_start=700, sweep_len=1200)
    sim.make_currentscape_plot(amp=0.5, time1=1000,time2=1075,stim_start=700, sweep_len=1200)
    
"""




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


root_path_out =  '/mnt/Plots/GYmut_TF_distribution'
na12name = 'na12_R850P_3107' #'na12_HMM_TF100923'
mut_name = 'na12_R850P_3107' #'na12_R850P_3107', 

if not os.path.exists(root_path_out):
        os.mkdir(root_path_out)


vals = [1]#[0.6,0.75,1.25,1.5] #[0.1,0.25,0.4] #[0.5,2,3]
for i in vals:

        #GY: need to run with the WT that I made my mutations with for comparisons
        sim = tf.Na12Model_TF(ais_nav12_fac = 7, ais_nav16_fac = 7, nav12 = 4, nav16 = 3,
        na12name = na12name,
        mut_name = mut_name, 
        params_folder = './params/', 
        plots_folder = f'{root_path_out}/0209', pfx=f'{na12name}_{mut_name}')


        #soma
        wt_Vm1,wt_I1,wt_t1,wt_stim1 = sim.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
        
        #make FI Vs DvDt
        sim.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'{mut_name}_')
        
        #make currentscape plots
        sim.make_currentscape_plot(amp=0.5, time1=0,time2=100,stim_start=30, sweep_len=100)

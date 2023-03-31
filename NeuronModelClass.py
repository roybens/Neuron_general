# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 21:07:44 2021

@author: bensr
"""
import argparse
import numpy as np
from vm_plotter import *
from neuron import h
import os

class NeuronModel:
    def __init__(self, mod_dir = './Neuron_Model_HH/', 
    
    nav12=1,
                      nav16=1,
                      dend_nav12=1,
                      soma_nav12=1,
                      ais_nav12=1,
                      dend_nav16=1,
                      soma_nav16=1,
                      ais_nav16=1,
                      ais_ca = 1,
                      ais_KCa = 1,
                      axon_Kp=1,
                      axon_Kt =1,
                      axon_K=1,
                      axon_Kca =1,
                      axon_HVA = 1,
                      axon_LVA = 1,
                      node_na = 1,
                      soma_K=1,
                      dend_K=1,
                      gpas_all=1):
        run_dir = os.getcwd()

        os.chdir(mod_dir)
        self.h = h  # NEURON h
        print(f'running model at {os.getcwd()} run dir is {run_dir}')
        h.load_file("runModel.hoc")
        self.soma_ref = h.root.sec
        self.soma = h.secname(sec=self.soma_ref)
        self.sl = h.SectionList()
        self.sl.wholetree(sec=self.soma_ref)
        self.nexus = h.cell.apic[66]
        self.dist_dend = h.cell.apic[91]
        self.ais = h.cell.axon[0]
        self.axon_proper = h.cell.axon[1]
        h.dend_na12 = 0.012/2
        h.dend_na16 = h.dend_na12
        h.dend_k = 0.004226 * soma_K


        h.soma_na12 = 0.983955/10
        h.soma_na16 = h.soma_na12
        h.soma_K = 8.396194779331378477e-02 * soma_K

        h.ais_na16 = 4
        h.ais_na12 = 4
        h.ais_ca = 0.00990*4*ais_ca
        h.ais_KCa = 0.007104*ais_KCa

        h.node_na = 2 * node_na

        h.axon_KP = 0.973538 * axon_Kp
        h.axon_KT = 1.7 * axon_Kt
        h.axon_K = 1.021945 * axon_K
        h.axon_LVA = 0.0014 * axon_LVA
        h.axon_HVA = 0.00012 * axon_HVA
        h.axon_KCA = 1.8 * axon_Kca


        #h.cell.axon[0].gCa_LVAstbar_Ca_LVAst = 0.001376286159287454

        #h.soma_na12 = h.soma_na12/2
        h.naked_axon_na = h.soma_na16/5
        h.navshift = -10
        h.myelin_na = h.naked_axon_na
        h.myelin_K = 0.303472
        h.myelin_scale = 10
        h.gpas_all = 3e-5 * gpas_all
        h.cm_all = 1


        h.dend_na12 = h.dend_na12 * nav12 * dend_nav12
        h.soma_na12 = h.soma_na12 * nav12 * soma_nav12
        h.ais_na12 = h.ais_na12 * nav12 * ais_nav12

        h.dend_na16 = h.dend_na16 * nav16 * dend_nav16
        h.soma_na16 = h.soma_na16 * nav16 * soma_nav16
        h.ais_na16 = h.ais_na16 * nav16 * ais_nav16
        h.working()
        os.chdir(run_dir)
    def init_stim(self, sweep_len = 800, stim_start = 100, stim_dur = 500, amp = 0.3, dt = 0.1):
        # updates the stimulation params used by the model
        # time values are in ms
        # amp values are in nA

        h("st.del = " + str(stim_start))
        h("st.dur = " + str(stim_dur))
        h("st.amp = " + str(amp))
        h.tstop = sweep_len
        h.dt = dt
    def run_model(self, start_Vm = -72, dt= 0.1,rec_extra = False):
        h.dt=dt
        h.finitialize(start_Vm)
        timesteps = int(h.tstop/h.dt)

        Vm = np.zeros(timesteps)
        I = {}
        I['Na'] = np.zeros(timesteps)
        I['Ca'] = np.zeros(timesteps)
        I['K'] = np.zeros(timesteps)
        stim = np.zeros(timesteps)
        t = np.zeros(timesteps)
        if rec_extra:
            
            extra_Vms = {}
            extra_Vms['ais'] = np.zeros(timesteps)
            extra_Vms['nexus'] = np.zeros(timesteps)
            extra_Vms['dist_dend'] = np.zeros(timesteps)
            extra_Vms['axon'] = np.zeros(timesteps)

        for i in range(timesteps):
            Vm[i] = h.cell.soma[0].v
            I['Na'][i] = h.cell.soma[0](0.5).ina
            I['Ca'][i] = h.cell.soma[0](0.5).ica
            I['K'][i] = h.cell.soma[0](0.5).ik
            stim[i] = h.st.amp
            t[i] = i*h.dt / 1000
            if rec_extra:
                nseg = int(self.h.L/10)*2 +1  # create 19 segments from this axon section
                ais_end = 10/nseg # specify the end of the AIS as halfway down this section
                ais_mid = 4/nseg # specify the middle of the AIS as 1/5 of this section 
                extra_Vms['ais'][i] = self.ais(ais_mid).v
                extra_Vms['nexus'][i] = self.nexus(0.5).v
                extra_Vms['dist_dend'][i] = self.dist_dend(0.5).v
                extra_Vms['axon'][i]=self.axon_proper(0.5).v
            h.fadvance()
        if rec_extra:
            return Vm, I, t, stim,extra_Vms
        else:
            return Vm, I, t, stim


#######################
# MAIN
#######################

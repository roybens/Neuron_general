from Na12HMMModel_TF import *
import matplotlib.pyplot as plt
import numpy as np
import NrnHelper as NH
from neuron import h
import time
import efel
efel.api.setDoubleSetting('Threshold', -40) #15 originally. ##TF022625 changed to -5 for kevin response to reviewers
import pandas as pd
import math
from scipy.signal import find_peaks

def get_sim_volt_values(sim,mut_name,rec_extra = False,dt = 0.005,stim_amp = 0.9): #originally had mutant_name, changed to mut_name 121223TF #dt=0.005 Original stim_amp=0.5 original

    # sim = Na12Model_TF(mutant_name)
    #sim = Na12Model_TF(mut_name)
    sim.dt= dt
    #sim.make_het()
    rec_extra = True
    sim.l5mdl.init_stim(amp=stim_amp)
    if rec_extra:
        Vm, I, t, stim,extra_vms = sim.l5mdl.run_model(dt=dt,rec_extra = rec_extra)

        sim.extra_vms = extra_vms
    else:
        Vm, I, t, stim = sim.l5mdl.run_model(dt=dt)

        extra_vms = {}

    return Vm,t,extra_vms,I,stim


def get_sim_volt_valuesTF(sim,mut_name,dt = 0.005,stim_amp = 0.5): #originally had mutant_name, changed to mut_name 121223TF #dt=0.005 Original

    # sim = Na12Model_TF(mutant_name)
    #sim = Na12Model_TF(mut_name)
    sim.dt= dt
    #sim.make_het()
    rec_extra = False
    sim.l5mdl.init_stim(amp=stim_amp)
    if rec_extra:
        Vm, I, t, stim,_ = sim.l5mdl.run_sim_model(dt=dt)

        # sim.extra_vms = extra_vms
    else:
        Vm, I, t, stim,_ = sim.l5mdl.run_sim_model(dt=dt)

        # extra_vms = {}

    return Vm,t,I,stim


def get_features(sim,prefix=None,mut_name = 'na12annaTFHH2',rec_extra=True): #added sim_config to allow run_sim_model instead of run_model 011924TF
    print("running routine")
    dt=0.005#0.1#0.005
    Vm,t,extra_vms,_,__ = get_sim_volt_values(sim,mut_name,rec_extra=rec_extra)
    # Vm,t,I,_ = get_sim_volt_valuesTF(sim,mut_name)
    #creating the trace file
    stim_start = 200 #100 original
    stim_end = 1900 #800 original
    trace={}
    trace = {'T':t,'V':Vm,'stim_start':[stim_start],'stim_end':[stim_end]}
    trace['T']= trace['T'] * 1000
    #for neu
    # feature_list= ['AP_height','AP_width','AP1_peak','AP1_width','Spikecount','all_ISI_values'] #original
    feature_list= ['AP_height','AP_width','AP1_peak','AP1_width','Spikecount','all_ISI_values'] ## 022525 abbreviated features for kevin response to reviewers
    
    traces = [trace]
    features = efel.getFeatureValues(traces,feature_list)
    
    ###Plotting Voltages to debug not getting enough spikes ##TF111524
    # plt.plot(trace['T'], trace['V'])
    # plt.xlabel('Time (ms)')
    # plt.ylabel('Voltage (mV)')
    # plt.title('Voltage vs Time')
    # plt.savefig('ZZZZZZZZZZZZZ_OGrun_voltage_vs_time5.pdf', format='pdf')  # Replace with your desired filename
    # plt.close()
    ###Plotting Voltages to debug not getting enough spikes ##TF111524

    try:
        features[0]['ISI mean'] =features[0]['all_ISI_values'].mean()
    except Exception as e:
        features[0]['ISI mean'] = 0
    features[0]['AP_height'] =features[0]['AP_height'].mean()
    features[0]['AP_width'] =features[0]['AP_width'][0].mean()
    features[0]['AP1_peak'] =features[0]['AP1_peak'][0]
    features[0]['AP1_width'] =features[0]['AP1_width'][0]
    features[0]['Spikecount'] =features[0]['Spikecount'][0]
    #import pdb; pdb.set_trace()
    #for dv/dt Peak 1 and Peak 2 and sum
    spike_count= features[0]['Spikecount']
    isi_values = features[0]['all_ISI_values']
    median_spike = int(math.floor(spike_count/2)) + 1
    #median spike location
    print(f'Length of isi_values {len(isi_values)}')
    print(f'isi_values: {isi_values}')
    print(f'Spike Count = {spike_count}')

    start = int((stim_start + isi_values[0:median_spike-1].sum())/dt) #original    #dividing by dt to get into same unit
    start2 = int((stim_start + isi_values[0:4].sum())/dt)    #dividing by dt to get into same unit
    try:
        # end = start + int(isi_values[median_spike]/dt)
        end = 380000
    except Exception as e:
        end=400000
        print("There were not enough spikes to calculate median isi")

    volt_segment = Vm[start:end] #original
    
    
    # startdt=int(stim_start/dt)
    # enddt=int(stim_end/dt)
    # volt_segment = Vm[startdt:enddt] ##TF022625 calculate dvdt from stim_start to stim_end rather than use isi median to find range
    dvdt = np.gradient(volt_segment)/dt
    ##DEBUG plot of dvdt
    # fig,axs = plt.subplots(1,1)
    # axs.plot(Vm,dvdt,color='red',linewidth=0.5)
    # fig.savefig(f'{mut_name}_getfeaturesDVDT.pdf')

    # curr_peaks_indices,curr_peaks_values= find_peaks(dvdt,height = 100) ##original
    curr_peaks_indices,curr_peaks_values= find_peaks(dvdt,height = 10) ##TF022625 reducing height for kevin response to reviewers
    print(f'start: {start}, start2:{start2}, end: {end}')
    print(f'volt_segment: {volt_segment}')
    print(f'dvdt: {dvdt}')
    print(f'curr_peaks_indices: {curr_peaks_indices}')
    print(f'curr_peaks_values: {curr_peaks_values}')
    features[0]['dvdt Peak1 Height'] = curr_peaks_values['peak_heights'][0]
    features[0]['dvdt Peak1 Voltage'] = volt_segment[curr_peaks_indices[0]] 
    features[0]['dvdt Peak2 Height'] = curr_peaks_values['peak_heights'][-1]
    features[0]['dvdt Peak2 Voltage'] = volt_segment[curr_peaks_indices[-1]]
    features[0]['dvdt Threshold'] = volt_segment[np.where(dvdt>1)[0][0]]

    positive_slope_indices = np.where(dvdt > 1)[0]
    if len(positive_slope_indices) > 0:
        threshold_index = positive_slope_indices[0]
        features[0]['dvdt Threshold_DEBUG'] = volt_segment[threshold_index]
    else:
        features[0]['dvdt Threshold_DEBUG'] = None
    
    if rec_extra:
    #for ais
        trace['V'] = extra_vms['ais']
        feat_list = ['Spikecount']
        traces = [trace]
        feature_ais = efel.getFeatureValues(traces,feat_list)
        features[0]['ais spikecount'] =feature_ais[0]['Spikecount']
        features[0]['ais spikecount'] =features[0]['ais spikecount'][0]
        
        #for nexus
        trace['V'] = extra_vms['nexus']
        feat_list = ['Spikecount']
        traces = [trace]
        feature_nex = efel.getFeatureValues(traces,feat_list)
        features[0]['nex spikecount'] =feature_nex[0]['Spikecount']
        features[0]['nex spikecount'] =features[0]['nex spikecount'][0]
        
        #for dist_dend
        trace['V'] = extra_vms['dist_dend']
        feat_list = ['Spikecount']
        traces = [trace]
        feature_disdend = efel.getFeatureValues(traces,feat_list)
        features[0]['disdend spikecount'] =feature_disdend[0]['Spikecount']
        features[0]['disdend spikecount'] =features[0]['disdend spikecount'][0]
    
    features = pd.DataFrame(features)
    features = features.drop(columns =['all_ISI_values'])
    features.insert(0,'Type',mut_name)
    with open (f'{prefix}_efel.csv','w') as f:
        features.to_csv(f,index=False)
    f.close()
    #features.to_csv(f'{paramlog_folder_path}/combined_paramlogs_{out_sfx}.csv', index=False) #Modify for saving features to csv
    return features
    




# mut_names = ['R853Q','E1211K','A1773T','G879R','A880S','A427D','E430A','E999K','E1211K','E1880K','G879R',
#            'K1260E','K1260Q','M1879T','R571H','R850P','R1319L','R1626Q','R1882L','R1882Q','S1780I','Y816F','na12WT2']

mut_names = ['na12_HMM_TF100923']
mut_not_found = {}
feature_row=None
for mut_name in mut_names:
    try:
        feature_row = get_features(mutant_name=mut_name)
        with open('efel_features.csv', 'a') as f:
            feature_row.to_csv(f, header=f.tell()==0,index=False) #bug needs an existing file

    except Exception as e:
        print(e)
        mut_not_found[mut_name] = e




def get_featuresTF(sim, prefix=None, mut_name='na12annaTFHH2', rec_extra=True):
    print("running routine")
    dt = 0.005
    Vm, t, extra_vms, _, __ = get_sim_volt_values(sim, mut_name, rec_extra=rec_extra)
    stim_start = 200
    stim_end = 1900
    trace = {'T': t, 'V': Vm, 'stim_start': [stim_start], 'stim_end': [stim_end]}
    trace['T'] = trace['T'] * 1000

    # Set a custom spike detection threshold
    trace['threshold'] = [-20]  # Set the threshold to -20 mV

    feature_list = ['AP_height', 'AP_width', 'AP1_peak', 'AP1_width', 'Spikecount', 'all_ISI_values']
    traces = [trace]
    features = efel.getFeatureValues(traces, feature_list)

    ### Plotting Voltages to debug not getting enough spikes
    plt.plot(trace['T'], trace['V'])
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.title('Voltage vs Time')
    plt.savefig('voltage_vs_time_debug.pdf', format='pdf')  # Replace with your desired filename
    plt.close()
    ### Plotting Voltages to debug not getting enough spikes

    if features and features[0]:
        try:
            features[0]['ISI mean'] = features[0]['all_ISI_values'].mean() if 'all_ISI_values' in features[0] and features[0]['all_ISI_values'] is not None else 0
        except Exception as e:
            features[0]['ISI mean'] = 0

        try:
            features[0]['AP_height'] = features[0]['AP_height'].mean() if 'AP_height' in features[0] and features[0]['AP_height'] is not None else 0
        except Exception as e:
            features[0]['AP_height'] = 0

        try:
            features[0]['AP_width'] = features[0]['AP_width'][0].mean() if 'AP_width' in features[0] and features[0]['AP_width'] is not None else 0
        except Exception as e:
            features[0]['AP_width'] = 0

        try:
            features[0]['AP1_peak'] = features[0]['AP1_peak'][0] if 'AP1_peak' in features[0] and features[0]['AP1_peak'] is not None else 0
        except Exception as e:
            features[0]['AP1_peak'] = 0

        try:
            features[0]['AP1_width'] = features[0]['AP1_width'][0] if 'AP1_width' in features[0] and features[0]['AP1_width'] is not None else 0
        except Exception as e:
            features[0]['AP1_width'] = 0

        try:
            features[0]['Spikecount'] = features[0]['Spikecount'][0] if 'Spikecount' in features[0] and features[0]['Spikecount'] is not None else 0
        except Exception as e:
            features[0]['Spikecount'] = 0

        spike_count = features[0]['Spikecount']
        isi_values = features[0]['all_ISI_values'] if 'all_ISI_values' in features[0] and features[0]['all_ISI_values'] is not None else []
        median_spike = int(math.floor(spike_count / 2)) + 1

        print(f'Length of isi_values: {len(isi_values)}')
        print(f'isi_values: {isi_values}')
        print(f'Spike Count = {spike_count}')

        if spike_count >= 2 and len(isi_values) >= median_spike:
            start = int((stim_start + sum(isi_values[0:median_spike - 1])) / dt)
            try:
                end = start + int(isi_values[median_spike] / dt)
            except Exception as e:
                end = 10000

            volt_segment = Vm[start:end]
            if len(volt_segment) > 1:
                dvdt = np.gradient(volt_segment) / dt
            else:
                dvdt = np.array([])  # Handle case where segment is too small
        else:
            print("Not enough spikes to calculate median ISI")
            dvdt = np.array([])  # Handle case where there are not enough spikes
    else:
        print(f"No features detected for {prefix}_{mut_name}")
        features = [{}]
        dvdt = np.array([])  # Handle case where no features are detected

    return features, dvdt
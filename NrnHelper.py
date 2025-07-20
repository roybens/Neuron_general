import json
import os
import glob
import tempfile
import subprocess
from scipy.signal import find_peaks
from vm_plotter import plot_stim_volts_pair
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from scalebary import add_scalebar
my_dpi = 96
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
#plt.rcParams['font.sans-serif'] = "Arial"
#plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
tick_major = 6
tick_minor = 4
plt.rcParams["xtick.major.size"] = tick_major
plt.rcParams["xtick.minor.size"] = tick_minor
plt.rcParams["ytick.major.size"] = tick_major
plt.rcParams["ytick.minor.size"] = tick_minor
font_small =9
font_medium = 13
font_large = 14
plt.rc('font', size=font_small)          # controls default text sizes
plt.rc('axes', titlesize=font_medium)    # fontsize of the axes title
plt.rc('axes', labelsize=font_medium)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=font_small)    # fontsize of the tick labels
plt.rc('ytick', labelsize=font_small)    # fontsize of the tick labels
plt.rc('legend', fontsize=font_small)    # legend fontsize
plt.rc('figure', titlesize=font_large)   # fontsize of the figure title
"""
ntimestep = 10000
dt = 0.02
def_times = np.array([dt for i in range(ntimestep)])
def_times = np.cumsum(def_times)
"""
def cm_to_in(cm):
    return cm/2.54




def get_fi_curve(mdl,s_amp,e_amp,nruns,wt_data=None,wt2_data=None, ax1=None,fig = None,dt = 0.01,fn = './Plots/ficurve.pdf',epochlabel='500ms'):
    all_volts = []
    npeaks = []
    x_axis = np.linspace(s_amp,e_amp,nruns)
    stim_length = int(600/dt)
    stim_length2 = int(1000/dt)

    # This makes sure red is always for the homozygous, blue for heterozygous and black for WT
    if wt_data is None:     #Only WT
        Color = 'black'
        Label = 'WT'
    elif wt2_data is None:  #WT vs Het
        Color = 'red'
        Label = 'Mutant'
    else:                   # Wt vs Het vs Homozygous
        Color = 'red'
        Label = 'Homozygous'

    stim_length2 = int(1000/dt)

    # This makes sure red is always for the homozygous, blue for heterozygous and black for WT
    if wt_data is None:     #Only WT
        Color = 'black'
        Label = 'WT'
    elif wt2_data is None:  #WT vs Het
        Color = 'red'
        Label = 'Mutant'
    else:                   # Wt vs Het vs Homozygous
        Color = 'red'
        Label = 'Homozygous'

    for curr_amp in x_axis:
        mdl.init_stim(amp = curr_amp,dt = dt)
        mdl.init_stim(amp = curr_amp,dt = dt)
        curr_volts,_,_,_ = mdl.run_model()
        #curr_peaks,_ = find_peaks(curr_volts[:stim_length],height = -20)
        curr_peaks,_ = find_peaks(curr_volts[:stim_length2],height = -30) #modified for na16 TTX experiments
        #curr_peaks,_ = find_peaks(curr_volts[:stim_length],height = -20)
        curr_peaks,_ = find_peaks(curr_volts[:stim_length2],height = -30) #modified for na16 TTX experiments
        all_volts.append(curr_volts)
        npeaks.append(len(curr_peaks))
    print(npeaks) #spikes at each stim current for FI curve
    print(npeaks) #spikes at each stim current for FI curve
    if ax1 is None:
        fig,ax1 = plt.subplots(1,1)
        ax1.plot(x_axis,npeaks,marker = 'o',markersize=1.5,linestyle = '-',color = Color, label = Label )
        ax1.plot(x_axis,npeaks,marker = 'o',markersize=1.5,linestyle = '-',color = Color, label = Label )
    ax1.set_title('FI Curve')
    ax1.set_xlabel('Stim [nA]')
    ax1.set_ylabel(f'nAPs for {epochlabel} epoch')
    
    ## Set min/max and axes manually
    # ymin=0
    # ymax=40
    # ax1.set_ylim(ymin,ymax)
    # ax1.set_yticks([0,5,10,15,20,25,30,35])
    
    ax1.set_ylabel(f'nAPs for {epochlabel} epoch')
    
    ## Set min/max and axes manually
    # ymin=0
    # ymax=40
    # ax1.set_ylim(ymin,ymax)
    # ax1.set_yticks([0,5,10,15,20,25,30,35])
    
    if wt_data is None:
        fig.show()
        fig.savefig(fn)
        fig.show()
        fig.savefig(fn)
        return npeaks
    else:
        ax1.plot(x_axis,wt_data,marker = 'o',markersize=1.5,linestyle = '-',color = 'black', label = 'WT') #mutant will be red
        
        ## Set min/max and axes manually
        # ymin=0
        # ymax=40
        # ax1.set_ylim(ymin,ymax)
        # ax1.set_yticks([0,5,10,15,20,25,30,35])
        
        if wt2_data is not None:
          ax1.plot(x_axis,wt2_data,marker = 'o',markersize=1.5, linestyle='-', color = 'blue', label= 'Heterozygous') #plots additional FI curve that you must supply array
          
          ## Set min/max and axes manually          
        #   ymin=0
        #   ymax=40
        #   ax1.set_ylim(ymin,ymax)
        #   ax1.set_yticks([0,5,10,15,20,25,30,35])
        
        #ax1.plot(x_axis,wt_data,'black')
    
    ##TF092724 Added to standardize Axes for Kevin's paper
    ## Set min/max and axes manually
    # ymin=0
    # ymax=40
    # ax1.set_ylim(ymin,ymax)
    # ax1.set_yticks([0,5,10,15,20,25,30,35])
        ax1.legend(loc='best', fontsize=8, markerscale = 3)
        ax1.plot(x_axis,wt_data,marker = 'o',markersize=1.5,linestyle = '-',color = 'black', label = 'WT') #mutant will be red
        
        ## Set min/max and axes manually
        # ymin=0
        # ymax=40
        # ax1.set_ylim(ymin,ymax)
        # ax1.set_yticks([0,5,10,15,20,25,30,35])
        
        if wt2_data is not None:
          ax1.plot(x_axis,wt2_data,marker = 'o',markersize=1.5, linestyle='-', color = 'blue', label= 'Heterozygous') #plots additional FI curve that you must supply array
          
          ## Set min/max and axes manually          
        #   ymin=0
        #   ymax=40
        #   ax1.set_ylim(ymin,ymax)
        #   ax1.set_yticks([0,5,10,15,20,25,30,35])
        
        #ax1.plot(x_axis,wt_data,'black')
    
    ##TF092724 Added to standardize Axes for Kevin's paper
    ## Set min/max and axes manually
    # ymin=0
    # ymax=40
    # ax1.set_ylim(ymin,ymax)
    # ax1.set_yticks([0,5,10,15,20,25,30,35])
    ax1.legend(loc='best', fontsize=8, markerscale = 3)
    fig.show()
    fig.savefig(fn)
    return(npeaks)


def plot_dvdt_from_volts(volts,dt,axs=None,clr = 'black',skip_first = False): #red #99023c #blue #6cc9ff #007dbc
    if skip_first:
        curr_peaks,_ = find_peaks(volts,height = -20)
        volts = volts[curr_peaks[0]+int(3/dt):]
    if axs is None:
        fig,axs = plt.subplots(1,1)
    dvdt = np.gradient(volts)/dt 
    
    # print(volts)
    # print(dt)
    # print(dvdt)
    # print(type(volts))
    # print(len(volts))
    # print(type(dt))
    # print(type(dvdt))
    # print(len(dvdt))
    #dvdt = np.gradient(volts)/dt
    
    axs.plot(volts, dvdt, color = clr, linewidth=0.5)
    #axs.plot(volts[1:20000], dvdt[1:20000], color = clr)#plot first peak only

    return axs

#plot first AP only
def plot_dvdt_from_volts_firstpeak(volts,dt,axs=None,clr = 'black',skip_first = False): #red #99023c #blue #6cc9ff #007dbc
    if skip_first:
        curr_peaks,_ = find_peaks(volts,height = -20)
        volts = volts[curr_peaks[0]+int(3/dt):]
    if axs is None:
        fig,axs = plt.subplots(1,1)
    dvdt = np.gradient(volts)/dt 
    
    # print(volts)
    # print(dt)
    # print(dvdt)
    # print(type(volts))
    # print(len(volts))
    # print(type(dt))
    # print(type(dvdt))
    # print(len(dvdt))
    #dvdt = np.gradient(volts)/dt
    
    #axs.plot(volts, dvdt, color = clr)
    axs.plot(volts[1:12500], dvdt[1:12500], color = clr)#plot first peak only [1:20000] was original

    return axs

def plot_dvdt_from_volts_wtvmut(volts,wt_Vm,dt,axs=None,het_Vm=None,clr = 'red',skip_first = False): #red #99023c #blue #6cc9ff #007dbc
    if skip_first:
        curr_peaks,_ = find_peaks(volts,height = -20)
        volts = volts[curr_peaks[0]+int(3/dt):]
    if axs is None:
        fig,axs = plt.subplots(1,1)
    dvdtwt = np.gradient(wt_Vm)/dt
    dvdt = np.gradient(volts)/dt
    if het_Vm is not None:
        dvdthet = np.gradient(het_Vm)/dt
     
    
    # print(volts)
    # print(dt)
    # print(dvdt)
    # print(type(volts))
    # print(len(volts))
    # print(type(dt))
    # print(type(dvdt))
    # print(len(dvdt))
    #dvdt = np.gradient(volts)/dt
    
    #axs.plot(volts, dvdt, color = clr)
    

    # Plot the dV/dt curves
     #plot first peak only [1:20000] was original
    axs.plot(wt_Vm, dvdtwt, color='black', alpha=0.8, linewidth=0.5, label='Wild Type')
    if het_Vm is not None:
        axs.plot(het_Vm, dvdthet, color='cadetblue', alpha=0.8, linewidth=0.5, label='Heterozygote')
        axs.plot(volts, dvdt, color=clr, linewidth=0.5, label='Homozygous')
    else:
        axs.plot(volts, dvdt, color=clr, linewidth=0.5, label='Mutant')

    # Add title, axis labels, and legend
    axs.set_title("dV/dt vs Membrane Voltage", fontsize=8)
    axs.set_xlabel("Membrane Voltage (mV)", fontsize=8)
    axs.set_ylabel("dV/dt (mV/ms)", fontsize=8)
    axs.legend(loc="best", fontsize=7, markerscale = 2)
    return axs

def plot_dg_dt(g,volts,dt,axs=None,clr = 'black'):
    if axs is None:
        fig,axs = plt.subplots(1,1)
    dgdt = np.gradient(g)/dt
    axs.plot(volts, dgdt, color = clr)

def plot_extra_volts(t,extra_vms,axs = None,clr = 'black'):
    if axs is None:
        fig,axs = plt.subplots(3,figsize=(cm_to_in(8),cm_to_in(23)))
    axs[0].plot(t,extra_vms['ais'], label='ais', color=clr,linewidth=1)
    axs[0].locator_params(axis='x', nbins=5)
    axs[0].locator_params(axis='y', nbins=8)
    axs[0].set_title('AIS')
    axs[1].plot(t,extra_vms['nexus'], label='nexus', color=clr,linewidth=1)
    axs[1].locator_params(axis='x', nbins=5)
    axs[1].locator_params(axis='y', nbins=8)
    axs[1].set_title('Nexus')
    axs[2].plot(t,extra_vms['dist_dend'], label='dist_dend', color=clr,linewidth=1)
    axs[2].locator_params(axis='x', nbins=5)
    axs[2].locator_params(axis='y', nbins=8)
    axs[2].set_title('dist_dend')


def plot_input_resistance(self, stim_amps, dt=0.02, axs=None, plot_fn='_', rec_extra=False, stim_dur=500, v_time=150, clr='black'):
    """
    Plots voltage traces for different stimulus amplitudes and computes input resistance.
    Top subplot: Positive current voltage traces only
    Middle subplot: All voltage traces  
    Bottom subplot: Input resistance calculation
    """
    # Consistent font sizes
    label_fontsize = 8
    title_fontsize = 10
    legend_fontsize = 5
    tick_fontsize = 6

    if axs is None:
        fig, axs = plt.subplots(3, 1, figsize=(cm_to_in(15), cm_to_in(22.5)), sharex=False)
    else:
        fig = axs[0].figure

    ## Plot voltage over time
    voltages_at_time = []
    baseline_voltage = None
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(stim_amps)))

    for i, stim_amp in enumerate(stim_amps):
        ap_t, Vm = self.plot_stim(
            stim_amp=stim_amp, dt=dt, clr=clr, plot_fn=f'{plot_fn}_{stim_amp}', 
            axs=axs[1], rec_extra=rec_extra, stim_dur=stim_dur
        )
        
        # EXTENSIVE DEBUG - Check what we're actually getting from NEURON
        print(f"=== VOLTAGE DEBUG for {stim_amp} nA ===")
        
        
        # Get baseline voltage (before stimulus, around 50ms)
        # Convert time to seconds since self.t is in seconds
        baseline_idx = np.argmin(np.abs(self.t - 50/1000))  # 50ms = 0.05s
        baseline_vm_this_trace = Vm[baseline_idx]
        
        # Get steady-state voltage during stimulus
        # Convert v_time (ms) to seconds
        steady_idx = np.argmin(np.abs(self.t - v_time/1000))  # Convert ms to seconds
        steady_vm_this_trace = Vm[steady_idx]
        
        # print(f"Baseline time: {self.t[baseline_idx]:.3f}ms, Baseline Vm: {baseline_vm_this_trace:.6f}")
        # print(f"Steady time: {self.t[steady_idx]:.3f}ms, Steady Vm: {steady_vm_this_trace:.6f}")
        
        # Use first trace baseline for all calculations
        if baseline_voltage is None:
            baseline_voltage = baseline_vm_this_trace
            print(f"*** SETTING BASELINE from first trace: {baseline_voltage:.6f} ***")
        
        # DEBUG: Check what gets appended to voltages_at_time
        # print(f"APPENDING TO voltages_at_time: {steady_vm_this_trace:.6f}")
        voltages_at_time.append(steady_vm_this_trace)
        # print(f"voltages_at_time after append: {[f'{v:.6f}' for v in voltages_at_time]}")
        
        # Plot all traces in middle subplot (axs[1])
        axs[1].plot(self.t, Vm, label=f'{stim_amp} nA', linewidth=0.8, 
                    color=colors[i], zorder=len(stim_amps)-i)
        
        # Plot positive currents in the top subplot (axs[0])
        if stim_amp > 0:
            # Find index for 300ms (0.3 seconds)
            max_time_idx = np.argmin(np.abs(self.t - 0.3))
            axs[0].plot(self.t[:max_time_idx], Vm[:max_time_idx], label=f'{stim_amp} nA', linewidth=0.8, 
                        color=colors[i], zorder=len(stim_amps)-i)
        
        # print(f'Current stim amp: {stim_amp}, Using baseline: {baseline_voltage:.6f}, Steady: {steady_vm_this_trace:.6f}')
        # print(f"=======================")

    # Format the top subplot for positive currents only
    # axs[0].axvline(x=50/1000, color='red', linestyle='--', linewidth=0.5, alpha=0.7, label='Baseline')
    # axs[0].axvline(x=v_time/1000, color='black', linestyle=':', linewidth=0.5, zorder=100, label='Measurement')
    axs[0].set_ylabel('Vm (mV)', fontsize=label_fontsize)
    axs[0].set_title('Voltage responses to positive step currents', fontsize=title_fontsize)
    axs[0].tick_params(axis='both', labelsize=tick_fontsize)
    handles, labels = axs[0].get_legend_handles_labels()
    filtered = [(h, l) for h, l in zip(handles, labels) if l.endswith('nA')]
    if filtered:
        handles, labels = zip(*filtered)
        axs[0].legend(handles, labels, fontsize=legend_fontsize, loc='center left', bbox_to_anchor=(1.1, 0.5), borderaxespad=0., handlelength=2)
    # Add horizontal blue lines at -45mV and 15mV
    axs[0].axhline(y=-45, color='blue', linewidth=0.5, linestyle=':')
    axs[0].axhline(y=15, color='blue', linewidth=0.5, linestyle=':')

    # Format the middle subplot for all voltage traces
    axs[1].axvline(x=50/1000, color='red', linestyle='--', linewidth=0.5, alpha=0.7, label='Baseline')
    axs[1].axvline(x=v_time/1000, color='black', linestyle=':', linewidth=0.5, zorder=100, label='Measurement')
    axs[1].set_ylabel('Vm (mV)', fontsize=label_fontsize)
    axs[1].set_title('Voltage responses to step currents', fontsize=title_fontsize)
    axs[1].tick_params(axis='both', labelsize=tick_fontsize)
    handles, labels = axs[1].get_legend_handles_labels()
    filtered = [(h, l) for h, l in zip(handles, labels) if l.endswith('nA')]
    if filtered:
        handles, labels = zip(*filtered)
        axs[1].legend(handles, labels, fontsize=legend_fontsize, loc='center left', bbox_to_anchor=(1.1, 0.5), borderaxespad=0., handlelength=2)

    ## Plot input resistances
    # Calculate resistance as (V_steady - V_baseline) / I_injected
    print(f"\n=== RESISTANCE CALCULATION DEBUG ===")
    print(f"Using baseline voltage: {baseline_voltage:.6f}")
    print(f"Voltages at measurement time: {[f'{v:.6f}' for v in voltages_at_time]}")
    print(f"Current amplitudes: {stim_amps}")
    
    resistances = []
    for j, (v_steady, i_amp) in enumerate(zip(voltages_at_time, stim_amps)):
        if abs(i_amp) > 1e-10:  # Avoid division by zero
            delta_v = v_steady - baseline_voltage  # Change from resting potential
            
            print(f"\nCurrent #{j}: {i_amp:.4f}nA")
            print(f"  Steady voltage: {v_steady:.6f}")
            print(f"  Baseline voltage: {baseline_voltage:.6f}")
            print(f"  Delta V: {delta_v:.6f}")
            
            # Try the calculation both ways to see which makes sense
            resistance_no_factor = abs(delta_v) / abs(i_amp)
            resistance_with_1000 = abs(delta_v) / abs(i_amp) * 1000
            
            print(f"  Resistance (no factor): {resistance_no_factor:.3f}")
            print(f"  Resistance (*1000): {resistance_with_1000:.3f}")
            
            # For now, let's use no factor and see what the debug shows
            resistance = resistance_no_factor
            resistances.append(resistance)
            
        else:
            resistances.append(np.nan)
            print(f"\nCurrent #{j}: {i_amp:.4f}nA - SKIPPED (too small)")
    
    print(f"\nFinal resistance values: {[f'{r:.3f}' for r in resistances if not np.isnan(r)]}")
    print(f"======================================\n")

    print(f"Baseline voltage: {baseline_voltage:.1f} mV")
    print(f"Resistance range: {min([r for r in resistances if not np.isnan(r)]):.0f} - {max([r for r in resistances if not np.isnan(r)]):.0f} MΩ")
    axs[2].plot(stim_amps, resistances, marker='o', markersize=2, linewidth=0.8, color='black', label='Resistance (MΩ)')
    axs[2].set_xlabel('Injected Current (nA)', fontsize=label_fontsize)
    axs[2].set_ylabel('Resistance (MΩ)', fontsize=label_fontsize, color='black')
    axs[2].tick_params(axis='y', labelcolor='black', labelsize=tick_fontsize)
    axs[2].tick_params(axis='x', labelsize=tick_fontsize)
    axs[2].set_title('Input Resistance', fontsize=title_fontsize)
    axs[2].grid(True, which='both', linestyle=':', linewidth=0.5)
    axs[2].set_xticks(stim_amps)
    axs[2].set_xticklabels([str(s) for s in stim_amps], fontsize=tick_fontsize, rotation=90) #rotation=90,

    ## Plot voltages at each stim current
    ax2 = axs[2].twinx()
    
    # FINAL DEBUG - Check the actual values being plotted
    print(f"\n=== FINAL VOLTAGE PLOTTING DEBUG ===")
    print(f"voltages_at_time values: {[f'{v:.6f}' for v in voltages_at_time]}")
    print(f"voltages_at_time min/max: {min(voltages_at_time):.6f} to {max(voltages_at_time):.6f}")
    print(f"Type of voltages_at_time: {type(voltages_at_time)}")
    print(f"Type of first element: {type(voltages_at_time[0])}")
    print(f"Baseline voltage for reference: {baseline_voltage:.6f}")
    print(f"=========================================\n")
    
    ax2.plot(stim_amps, voltages_at_time, marker='o', markersize=2, linewidth=0.8, color='deepskyblue', label=f'Vm at {v_time} ms')
    ax2.set_ylabel(f'Vm at {v_time} ms (mV)', fontsize=label_fontsize, color='deepskyblue')
    ax2.tick_params(axis='y', labelcolor='deepskyblue', labelsize=tick_fontsize)
    ax2.yaxis.set_ticks_position('right')
    ax2.yaxis.set_label_position('right')
    ax2.grid(False)
    ax2.spines['right'].set_visible(True)
    
    # Set reasonable voltage axis limits
    v_min, v_max = min(voltages_at_time), max(voltages_at_time)
    v_range = v_max - v_min
    ax2.set_ylim(v_min - 0.1*v_range, v_max + 0.1*v_range)

    fig.tight_layout()
    file_path_to_save = f'{self.plot_folder}/{plot_fn}_Rin.pdf'
    fig.savefig(file_path_to_save)
    return axs, stim_amps, voltages_at_time, resistances


def update_mech_from_dict(mdl,dict_fn,mechs,input_dict = False, param_name='a1_0'):
    if input_dict:
        param_dict = dict_fn
    else:
        with open(dict_fn) as f:
            data = f.read()
        param_dict = json.loads(data)
    print(f'updating {mechs} with {param_dict}')
    isUpdated = False
    for curr_sec in mdl.sl:
        # print(f'current section {curr_sec}') ###120523 TF
        if curr_sec.name() == 'cADpyr232_L5_TTPC1_0fb1ca4724[0].axon[0]': ##TF040224 if not axon[0], continues to for loop below
            # print('THIS IS AXON 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print(f'Current Mech {curr_mech} and current section {curr_sec}')
            # print('THIS IS AXON 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            ##TF052324/##
            # Update all parameters except gbar for the axon section. AIS gbar will get updated when update_mod_param called (dependent on nav12/16)
            for curr_mech in mechs:
                # print(f'Current Mech {curr_mech} and current section {curr_sec}') ###120523 TF
                if h.ismembrane(curr_mech, sec=curr_sec):
                    curr_name = h.secname(sec=curr_sec)
                    for seg in curr_sec:
                        for p_name in param_dict.keys():
                            hoc_cmd = f'{curr_name}.{p_name}_{curr_mech}({seg.x}) = {param_dict[p_name]}'
                            # print(f'hoc command {hoc_cmd}')
                            h(hoc_cmd)
            continue
            ##/TF05224##
            
        # Update all other sections other than axon[0]
        for curr_mech in mechs:
            # print(f'Current Mech {curr_mech} and current section {curr_sec}') ###120523 TF
            if h.ismembrane(curr_mech, sec=curr_sec):
                isUpdated = True
                curr_name = h.secname(sec=curr_sec)
                #sec = h.Section()

                #######Original
                # for p_name in param_dict.keys():
                #     hoc_cmd = f'{curr_name}.{p_name}_{curr_mech} = {param_dict[p_name]}'
                #     h(hoc_cmd)

                #in case we need to go per sec:
                  #  for seg in curr_sec:
                  #      hoc_cmd = f'{curr_name}.gbar_{channel}({seg.x}) *= {wt_mul}'
                  #      print(hocmd)

                ##TF040124 altering to update axon[0] to get ais correct and not apply blanket gbar to all segs
                # Overwrite gbar for other sections
                for p_name in param_dict.keys():
                    if curr_sec != 'cADpyr232_L5_TTPC1_0fb1ca4724[0].axon[0]':
                        hoc_cmd = f'{curr_name}.{p_name}_{curr_mech} = {param_dict[p_name]}'
                        h(hoc_cmd)#############################
                    
                    ## Multiply gbar for the specific axon segment
                    # else:
                    #     for seg in curr_sec:
                    #         print('this is the one **************************************************************************************************************************************************************')
                    #         hoc_cmd1 = f'{curr_name}.{p_name}_{curr_mech} = {param_dict[p_name]}'
                    #         h(hoc_cmd1)
                    #         print(f'hoc command 1 {hoc_cmd1}')
                    #         hoc_cmd = f'{curr_name}.gbar_{curr_mech}({seg.x}) *= {param_dict[p_name]}'
                    #         print(f'hoc command {hoc_cmd}')
                    #         h(hoc_cmd)
                    #         print('this is the one **************************************************************************************************************************************************************')
    if(not isUpdated):
        print("Havent Updated in any section")
    else: print("Updated !!!!")
    return param_dict

##TF030624 Update mech from dict function specifically for HH mod files
def update_mech_from_dict_HH(mdl,dict_fn,mechs,input_dict = False, param_name='a1_0'):
    if input_dict:
        param_dict = dict_fn
    else:
        with open(dict_fn) as f:
            data = f.read()
        param_dict = json.loads(data)
    print(f'updating {mechs} with {param_dict}')
    
    for curr_sec in mdl.sl:
        print(f'current section {curr_sec}') ###120523 TF
        for curr_mech in mechs:
            print(f'Current Mech {curr_mech}') ###120523 TF
            if h.ismembrane(curr_mech, sec=curr_sec):
                curr_name = h.secname(sec=curr_sec)
                #print(f'Current Name {curr_name}')###120523 TF
                #sec = h.Section()
                #print(sec)
                #print(eval(f'h.psection(sec=sec)'))
                #print(h.Section())

                for p_name in param_dict.keys():
                    # print(f' p name {p_name}') ###120523 TF
                    hoc_cmd = f'{curr_name}.{p_name} = {param_dict[p_name]}'
                    # print(f'hoc command {hoc_cmd}') ###120523 TF
                    h(hoc_cmd)
              
              
                #in case we need to go per sec:
                  #  for seg in curr_sec:
                  #      hoc_cmd = f'{curr_name}.gbar_{channel}({seg.x}) *= {wt_mul}'
                  #      print(hocmd)
    
    return param_dict

def update_mod_param(mdl,mechs,mltplr,gbar_name = 'gbar', print_flg =False):
    for curr_sec in mdl.sl:
        curr_name = h.secname(sec=curr_sec)
        for curr_mech in mechs:
            if h.ismembrane(curr_mech, sec=curr_sec):
                for seg in curr_sec:
                    hoc_cmd = f'{curr_name}.{gbar_name}_{curr_mech}({seg.x}) *= {mltplr}'
                    # print(hoc_cmd)
                    # print(f'this is the par value')
                    par_value = h(f'{curr_name}.{gbar_name}_{curr_mech}({seg.x})')
                    h(hoc_cmd)
                    assigned_value = h(f'{curr_name}.{gbar_name}_{curr_mech}({seg.x})')
                    # print(f'this is the assigned value')
                    #h(f'{curr_name}.{gbar_name}_{curr_mech}({seg.x})')
                   
                    # print(f'par_value before{par_value} and after {assigned_value}')
                    if print_flg:
                       print(f'{curr_name}_{curr_mech}_{seg}_par_value before {par_value} and after {assigned_value}')
                       print(f'**********##### There is now {mltplr} of {curr_mech}\n\n')

###############****************************##############################
##### CAUTION!!!! This function will continue multiplying the mechanism-level parameter every loop
##### That means you will get cumulative multiplication if you call this function multiple times!!!!!!!
# def multiply_param(mdl,mechs,p_name,multiplier):
#     '''Multiply a parameter for all sections and mechanisms in the model.
#     If the segment has already been assigned the value you're trying to multiply,
#     trying to reassign the section value will not work for PARAMETER/RANGE variables.
#     Instead, you need to multiply the value at each segment.'''
#     for curr_sec in mdl.sl:
#         for curr_mech in mechs:
#             if h.ismembrane(curr_mech, sec=curr_sec):
#                 curr_name = h.secname(sec=curr_sec)
#                 hoc_cmd = f'{curr_name}.{p_name}_{curr_mech} *= {multiplier}'
#                 #print(hoc_cmd)
#                 h(hoc_cmd)
##### CAUTION!!!
###############****************************##############################


def multiply_param(mdl, mechs, param_name, factor):
    """
    Robustly multiplies a mechanism's RANGE parameter by a factor.

    This function is idempotent. It caches the baseline value of a parameter
    on the first call and uses that baseline for all subsequent multiplications,
    preventing cumulative errors in loops. It correctly handles RANGE variables
    by iterating over all sections.

    Args:
        mdl (NeuronModel): The model instance, which must have a `_param_baselines` dict.
        mechs (list): A list of mechanism names (e.g., ['SKv3_1']).
        param_name (str): The name of the parameter to modify (e.g., 'mtaumul').
        factor (float): The factor to multiply the baseline by.
    """
    if factor is None:
        return

    for mech in mechs:
        try:
            full_param_name = f"{param_name}_{mech}"

            # 1. Check if we have a stored baseline for this parameter.
            if full_param_name not in mdl._param_baselines:
                # If not, find the first section with the mechanism to read the baseline.
                baseline_found = False
                for sec in mdl.sl:
                    if h.ismembrane(mech, sec=sec):
                        # Read the value from the first section we find.
                        baseline_value = getattr(sec, full_param_name)
                        mdl._param_baselines[full_param_name] = baseline_value
                        print(f"INFO: Caching baseline for {full_param_name}: {baseline_value} (from {sec.name()})")
                        baseline_found = True
                        break  # Stop after finding the first one.
                if not baseline_found:
                    print(f"WARNING: Mechanism '{mech}' not found in any section. Cannot multiply '{param_name}'.")
                    continue  # Move to the next mechanism in the list.

            # 2. Get the baseline value from our cache.
            baseline = mdl._param_baselines[full_param_name]

            # 3. Calculate the new value from the baseline and the factor.
            new_value = baseline * factor

            # 4. Set the new, absolute value on ALL sections that have the mechanism.
            updated_count = 0
            for sec in mdl.sl:
                if h.ismembrane(mech, sec=sec):
                    setattr(sec, full_param_name, new_value)
                    updated_count += 1
            
            if updated_count == 0:
                 print(f"WARNING: No sections updated for {full_param_name}. Mechanism may not be inserted.")

        except AttributeError:
            # This might catch the case where the parameter doesn't exist on the section object
            print(f"WARNING: Could not find parameter '{full_param_name}' on a section. Check mechanism and parameter names.")
        except Exception as e:
            print(f"ERROR: An unexpected error occurred while updating {full_param_name}: {e}")




def multiply_param_sec_seg(mdl, mechs, p_name, multiplier):
    '''Multiply a parameter for all sections and segments in the model.
    If the segment has already been assigned the value you're trying to multiply,
    you need to multiply the value at each segment for PARAMETER/RANGE variables.'''
    for curr_sec in mdl.sl:
        for curr_mech in mechs:
            if h.ismembrane(curr_mech, sec=curr_sec):
                for seg in curr_sec:
                    # Try to multiply at the segment level if the attribute exists
                    attr_name = f"{p_name}_{curr_mech}"
                    if hasattr(seg, attr_name):
                        setattr(seg, attr_name, getattr(seg, attr_name) * multiplier)
                # Also multiply at the section level in case some segments still use the section value
                curr_name = h.secname(sec=curr_sec)
                hoc_cmd = f'{curr_name}.{p_name}_{curr_mech} *= {multiplier}'
                h(hoc_cmd)

def offset_param(mdl,mechs,p_name,offset):
    for curr_sec in mdl.sl:
        for curr_mech in mechs:
            if h.ismembrane(curr_mech, sec=curr_sec):
                curr_name = h.secname(sec=curr_sec)
                hoc_cmd = f'{curr_name}.{p_name}_{curr_mech} += {offset}'
                print(hoc_cmd)
                h(hoc_cmd)
def update_param_value(mdl,mechs,p_name,value):
    for curr_sec in mdl.sl:
        for curr_mech in mechs:
            if h.ismembrane(curr_mech, sec=curr_sec):
                curr_name = h.secname(sec=curr_sec)
                hoc_cmd = f'{curr_name}.{p_name}_{curr_mech} = {value}'
                # print(hoc_cmd)
                h(hoc_cmd)










#### Emily's code
def update_channel(mdl, channel_name, channel, dict_fn, wt_mul, mut_mul):
    """
    channel_name: str e.g 'na16mut'
    channel: str e.g. 'na16'
    """
    with open(dict_fn) as f:
        data = f.read()
    param_dict = json.loads(data)
    for curr_sec in mdl.sl:
        if h.ismembrane(channel_name, sec=curr_sec):
            curr_name = h.secname(sec=curr_sec)
            for seg in curr_sec:
                hoc_cmd = f'{curr_name}.gbar_{channel_name}({seg.x}) *= {mut_mul}'
                #print(hoc_cmd)
                h(hoc_cmd)
            for p_name in param_dict.keys():
                hoc_cmd = f'{curr_name}.{p_name} = {param_dict[p_name]}'
                #print(hoc_cmd)
                h(hoc_cmd)
        if h.ismembrane(channel, sec=curr_sec):
            curr_name = h.secname(sec=curr_sec)
            for seg in curr_sec:
                hoc_cmd = f'{curr_name}.gbar_{channel}({seg.x}) *= {wt_mul}'
                #print(hoc_cmd)
                h(hoc_cmd)


def update_K(mdl, channel_name, gbar_name, mut_mul):
    k_name = f'{gbar_name}_{channel_name}'
    prev = []
    for curr_sec in mdl.sl:
        if h.ismembrane(channel_name, sec=curr_sec):
            curr_name = h.secname(sec=curr_sec)
            for seg in curr_sec:
                hoc_cmd = f'{curr_name}.{k_name}({seg.x}) *= {mut_mul}'
                print(hoc_cmd)
                h(f'a = {curr_name}.{k_name}({seg.x})')  # get old value
                prev_var = h.a
                prev.append(f'{curr_name}.{k_name}({seg.x}) = {prev_var}')  # store old value in hoc_cmd
                h(hoc_cmd)
    return prev


def reverse_update_K(mdl, channel_name, gbar_name, prev):
    k_name = f'{gbar_name}_{channel_name}'
    index = 0
    for curr_sec in mdl.sl:
        if h.ismembrane(channel_name, sec=curr_sec):
            curr_name = h.secname(sec=curr_sec)
            for seg in curr_sec:
                hoc_cmd = prev[index]
                h(hoc_cmd)
                index += 1

def plot_stim(mdl, amp,fn,clr='blue'):
    mdl.init_stim(amp=amp)
    Vm, I, t, stim = mdl.run_model()
    plot_stim_volts_pair(Vm, f'Step Stim {amp}pA', file_path_to_save=f'./Plots/V1/{fn}_{amp}pA',times=t,color_str=clr)
    return I

def plot_FIs(fis, extra_cond = False):
    data = fis
    # save multiple figures in one pdf file
    filename= f'Plots/FI_plots.pdf'
    fig = plt.figure()
    x_axis, npeaks, name = data[0]
    plt.plot(x_axis, npeaks, label=name, color='black')
    # plot mut
    x_axis, npeaks, name = data[1]
    plt.plot(x_axis, npeaks, label=name, color='red')
    if extra_cond:
        # plot wtTTX
        x_axis, npeaks, name = data[2]
        plt.plot(x_axis, npeaks, label=name, color='black', linestyle='dashed')
        # plot mutTTX
        x_axis, npeaks, name = data[3]
        plt.plot(x_axis, npeaks, label=name, color='red', linestyle='dashed')

    plt.legend()
    plt.xlabel('Stim [nA]')
    plt.ylabel('nAPs for 600ms epoch')
    plt.title(f'FI Curve')
    fig.savefig(filename)


def plot_all_FIs(fis, extra_cond = False):
    for i in range(len(fis)):
        data = fis[i]
        # save multiple figures in one pdf file
        filename= f'Plots/FI_plots{i}.pdf'
        fig = plt.figure()
        x_axis, npeaks, name = data[0]
        plt.plot(x_axis, npeaks, label=name, color='black')
        # plot mut
        x_axis, npeaks, name = data[1]
        plt.plot(x_axis, npeaks, label=name, color='red')
        if extra_cond:
            # plot wtTTX
            x_axis, npeaks, name = data[2]
            plt.plot(x_axis, npeaks, label=name, color='black', linestyle='dashed')
            # plot mutTTX
            x_axis, npeaks, name = data[3]
            plt.plot(x_axis, npeaks, label=name, color='red', linestyle='dashed')

        plt.legend()
        plt.xlabel('Stim [nA]')
        plt.ylabel('nAPs for 500ms epoch')
        plt.title(f'FI Curve: for range {i}')
        fig.savefig(filename)
def scan12_16():
    for i12 in np.arange(0.5,1.5,0.1):
        for i16 in np.arange(0.5,1.5,0.1):
            sim = Na1612Model(nav12=i12, nav16=i16)
            sim.make_wt()
            fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
            sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
            NH.plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
            fn = f'./Plots/na1216_trials/vs_dvdt12_{i12}_16_{i16}.pdf'
            fig_volts.savefig(fn)

def get_spike_times(volts,times):
    inds,peaks = find_peaks(volts,height = -20)
    ans = [times[x] for x in inds]
    return ans















def plot_comprehensive_analysis(model, stim_amps=None, single_stim_amp=0.3, dt=0.02, 
                               plot_fn='comprehensive_analysis', rec_extra=False, 
                               stim_dur=500, v_time=150, clr='black',
                               currentscape_config=None, axon_config=None, save_individual=True):
    """
    Creates a comprehensive analysis plot combining:
    - Input resistance analysis (top 3 rows, full width, stacked vertically)
    - dV/dt phase plots (1 row, 2 plots side-by-side, each half width) 
    
    Parameters:
    -----------
    model : NeuronModel instance
        The neuron model to analyze
    stim_amps : list, optional
        Current amplitudes for input resistance analysis. 
        Default: [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
    single_stim_amp : float, optional
        Single current amplitude for dV/dt analysis (default: 0.3)
    dt : float, optional
        Time step for simulation (default: 0.02)
    plot_fn : str, optional
        Base filename for saving plots (default: 'comprehensive_analysis')
    rec_extra : bool, optional
        Whether to record extra locations (default: False)
    stim_dur : float, optional
        Stimulus duration in ms (default: 500)
    v_time : float, optional
        Time point for voltage measurements in ms (default: 150)
    clr : str, optional
        Color for single trace plots (default: 'black')
    currentscape_config : dict, optional
        Configuration for currentscape plot (kept for compatibility, but not used)
    axon_config : dict, optional
        Configuration for axon plot (kept for compatibility, but not used)
    save_individual : bool, optional
        Whether to save individual component plots (default: True)
        
    Returns:
    --------
    fig : matplotlib figure
        The combined figure
    results : dict
        Dictionary containing analysis results from each component
    """
    
    # Clear any existing figures to prevent memory leaks
    plt.close('all')
    
    # Default stimulus amplitudes for input resistance
    if stim_amps is None:
        stim_amps = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
    
    # Create the main figure with taller layout and minimize gap to title
    # Simplified layout: 4 rows without currentscape
    # Row 0-2: Input resistance (3 plots stacked, full width) - taller
    # Row 3: Voltage trace (left) and dV/dt vs V (right) - taller  
    fig = plt.figure(figsize=(cm_to_in(22), cm_to_in(50)))
    
    # Define grid layout: 4 rows with height ratios optimized for the content
    gs = fig.add_gridspec(4, 2, height_ratios=[2, 2, 2, 2], hspace=0.3, wspace=0.3, 
                         top=0.95, bottom=0.05)  # Minimize gap to title
    
    # Input resistance analysis - 3 plots stacked vertically, full width
    ax_rin1 = fig.add_subplot(gs[0, :])  # Positive currents only (full width)
    ax_rin2 = fig.add_subplot(gs[1, :])  # All voltage traces (full width)
    ax_rin3 = fig.add_subplot(gs[2, :])  # Resistance plot (full width)
    
    # Voltage trace and dV/dt analysis - 2 plots side-by-side, half width each
    ax_voltage_trace = fig.add_subplot(gs[3, 0])  # Voltage trace (left half)
    ax_dvdt_vs_v = fig.add_subplot(gs[3, 1])     # dV/dt vs V plot (right half)
    
    print("Starting comprehensive analysis (without currentscape)...")
    
    # Results dictionary to store analysis outputs
    results = {}
    
    # 1. INPUT RESISTANCE ANALYSIS
    print("1. Running input resistance analysis...")
    try:
        # For Na12Model_TF, we need to manually create input resistance analysis
        print("   Creating input resistance analysis for Na12Model_TF...")
        
        voltages_at_time = []
        baseline_voltage = None
        colors = plt.cm.coolwarm(np.linspace(0, 1, len(stim_amps)))
        
        for i, stim_amp in enumerate(stim_amps):
            # Use the model's plot_stim method
            ap_t, Vm = model.plot_stim(
                stim_amp=stim_amp, dt=dt, plot_fn=f'{plot_fn}_rin_{stim_amp}', 
                axs=None, rec_extra=rec_extra, stim_dur=stim_dur
            )
            
            # Get time array
            if hasattr(model, 't'):
                t_array = model.t
            elif hasattr(model.l5mdl, 't'):
                t_array = model.l5mdl.t
            else:
                # Create time array if not available
                t_array = np.arange(len(Vm)) * dt / 1000  # Convert ms to seconds
            
            # Get baseline and steady-state voltages
            baseline_idx = np.argmin(np.abs(t_array - 50/1000))  # 50ms baseline
            steady_idx = np.argmin(np.abs(t_array - v_time/1000))  # measurement time
            
            baseline_vm_this_trace = Vm[baseline_idx]
            steady_vm_this_trace = Vm[steady_idx]
            
            if baseline_voltage is None:
                baseline_voltage = baseline_vm_this_trace
            
            voltages_at_time.append(steady_vm_this_trace)
            
            # Plot traces
            ax_rin2.plot(t_array, Vm, label=f'{stim_amp} nA', linewidth=0.8, 
                        color=colors[i], zorder=len(stim_amps)-i)
            
            # Plot positive currents only in top subplot
            if stim_amp > 0:
                max_time_idx = np.argmin(np.abs(t_array - 0.3))
                ax_rin1.plot(t_array[:max_time_idx], Vm[:max_time_idx], label=f'{stim_amp} nA', linewidth=0.8, 
                           color=colors[i], zorder=len(stim_amps)-i)
        
        # Calculate resistances
        resistances = []
        for v_steady, i_amp in zip(voltages_at_time, stim_amps):
            if abs(i_amp) > 1e-10:
                delta_v = v_steady - baseline_voltage
                resistance = abs(delta_v) / abs(i_amp)
                resistances.append(resistance)
            else:
                resistances.append(np.nan)
        
        # Format plots
        ax_rin1.set_ylabel('Vm (mV)', fontsize=8)
        ax_rin1.set_title('Voltage responses to positive step currents', fontsize=10)
        ax_rin1.legend(fontsize=6)
        
        ax_rin2.axvline(x=50/1000, color='red', linestyle='--', linewidth=0.5, alpha=0.7)
        ax_rin2.axvline(x=v_time/1000, color='black', linestyle=':', linewidth=0.5)
        ax_rin2.set_ylabel('Vm (mV)', fontsize=8)
        ax_rin2.set_title('Voltage responses to step currents', fontsize=10)
        ax_rin2.legend(fontsize=6)
        
        # Plot resistance (black line) and add voltage vs current (blue line)
        ax_rin3.plot(stim_amps, resistances, marker='o', markersize=2, linewidth=0.8, color='black', label='Resistance')
        ax_rin3.set_xlabel('Injected Current (nA)', fontsize=8)
        ax_rin3.set_ylabel('Resistance (MΩ)', fontsize=8, color='black')
        ax_rin3.set_title('Input Resistance & Voltage Response', fontsize=10)
        ax_rin3.grid(True, alpha=0.3)
        ax_rin3.tick_params(axis='y', labelcolor='black')
        
        # Add twin axis for voltage vs current (blue line)
        ax_rin3_twin = ax_rin3.twinx()
        voltage_deltas = [v - baseline_voltage for v in voltages_at_time]
        ax_rin3_twin.plot(stim_amps, voltage_deltas, marker='s', markersize=2, linewidth=0.8, color='blue', label='ΔVm')
        ax_rin3_twin.set_ylabel('Voltage Change (mV)', fontsize=8, color='blue')
        ax_rin3_twin.tick_params(axis='y', labelcolor='blue')
        
        # Add legends for both lines
        lines1, labels1 = ax_rin3.get_legend_handles_labels()
        lines2, labels2 = ax_rin3_twin.get_legend_handles_labels()
        ax_rin3.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=6)
        
        results['input_resistance'] = {
            'stim_amps': stim_amps,
            'voltages': voltages_at_time,
            'resistances': resistances,
            'mean_resistance': np.nanmean(resistances) if resistances else None
        }
        
        print(f"   Mean input resistance: {results['input_resistance']['mean_resistance']:.1f} MΩ")
        
    except Exception as e:
        print(f"Error in input resistance analysis: {e}")
        results['input_resistance'] = {'error': str(e)}
    
    # 2. VOLTAGE TRACE AND dV/dT ANALYSIS
    print("2. Running voltage trace and dV/dt analysis...")
    try:
        # Get voltage trace for analysis using model's plot_stim method
        print("   Getting voltage trace for analysis...")
        ap_t, Vm_trace = model.plot_stim(
            stim_amp=single_stim_amp, dt=dt, plot_fn=f'{plot_fn}_voltage_trace',
            axs=None, rec_extra=rec_extra, stim_dur=stim_dur
        )
        
        # Get time array
        if hasattr(model, 't'):
            t_array = model.t
        elif hasattr(model.l5mdl, 't'):
            t_array = model.l5mdl.t
        else:
            t_array = np.arange(len(Vm_trace)) * dt / 1000  # Convert ms to seconds
        
        # Plot voltage trace (left subplot) - this replaces dV/dt vs time
        ax_voltage_trace.plot(t_array, Vm_trace, color=clr, linewidth=0.8)
        ax_voltage_trace.set_xlabel('Time (s)', fontsize=8)
        ax_voltage_trace.set_ylabel('Voltage (mV)', fontsize=8)
        ax_voltage_trace.set_title(f'Voltage Trace ({single_stim_amp} nA)', fontsize=10)
        ax_voltage_trace.grid(True, alpha=0.3)
        
        # Plot dV/dt vs V (right subplot)
        plot_dvdt_from_volts(Vm_trace, dt, axs=ax_dvdt_vs_v, clr=clr)
        ax_dvdt_vs_v.set_title('dV/dt vs Voltage', fontsize=10)
        ax_dvdt_vs_v.set_xlabel('Voltage (mV)', fontsize=8)
        ax_dvdt_vs_v.set_ylabel('dV/dt (mV/ms)', fontsize=8)
        
        # Calculate analysis metrics
        dvdt = np.gradient(Vm_trace) / dt
        peaks, _ = find_peaks(Vm_trace, height=-20)
        max_dvdt = np.max(dvdt)
        
        results['dvdt_analysis'] = {
            'voltage_trace': Vm_trace,
            'dvdt_trace': dvdt,
            'time': t_array,
            'num_spikes': len(peaks),
            'max_dvdt': max_dvdt,
            'spike_amplitude': np.max(Vm_trace) - np.min(Vm_trace) if len(peaks) > 0 else 0
        };
        
        print(f"   Number of spikes: {len(peaks)}")
        print(f"   Max dV/dt: {max_dvdt:.1f} mV/ms")
        print(f"   Spike amplitude: {results['dvdt_analysis']['spike_amplitude']:.1f} mV")
        
    except Exception as e:
        print(f"Error in voltage/dV/dt analysis: {e}")
        results['dvdt_analysis'] = {'error': str(e)}
    
    # Add overall title with minimal gap and improved layout
    fig.suptitle(f'Comprehensive Neuron Analysis (Input Resistance + dV/dt)', fontsize=16, y=0.97)
    
    # Adjust layout with minimal spacing
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for title
    
    # Save the comprehensive plot
    save_path = f'{model.plot_folder if hasattr(model, "plot_folder") else "."}/{plot_fn}_comprehensive.pdf'
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Comprehensive analysis saved to: {save_path}")
    
    # Save individual components if requested
    if save_individual:
        # Save dV/dt component
        if 'dvdt_analysis' in results and 'error' not in results['dvdt_analysis']:
            fig_dvdt, ax_dvdt_save = plt.subplots(1, 1, figsize=(cm_to_in(10), cm_to_in(8)))
            plot_dvdt_from_volts(results['dvdt_analysis']['voltage_trace'], dt, 
                               axs=ax_dvdt_save, clr=clr)
            ax_dvdt_save.set_title(f'dV/dt Analysis ({single_stim_amp} nA)')
            dvdt_path = f'{model.plot_folder if hasattr(model, "plot_folder") else "."}/{plot_fn}_dvdt.pdf'
            fig_dvdt.savefig(dvdt_path)
            plt.close(fig_dvdt)
            print(f"dV/dt analysis saved to: {dvdt_path}")
    
    print("Comprehensive analysis completed!")
    return fig, results

def combine_currentscape_pdfs(soma_pdf_pattern, axon_pdf_pattern, output_filename, 
                             plot_folder=".", title_prefix=""):
    """
    Combine soma and axon currentscape PDFs into a single document.
    
    Parameters:
    -----------
    soma_pdf_pattern : str
        File pattern or path for the soma currentscape PDF (e.g., "soma_currentscape*.pdf")
    axon_pdf_pattern : str
        File pattern or path for the axon currentscape PDF (e.g., "axon_currentscape*.pdf")
    output_filename : str
        Name for the combined output PDF file
    plot_folder : str, optional
        Directory containing the PDF files (default: ".")
    title_prefix : str, optional
        Prefix for the title page (default: "")
        
    Returns:
    --------
    str : Path to the combined PDF file, or None if unsuccessful
    """
    import os
    import glob
    
    try:
        # Try using PyPDF2 first (more common)
        try:
            from PyPDF2 import PdfMerger
            pdf_merger_available = True
        except ImportError:
            try:
                from pypdf import PdfMerger
                pdf_merger_available = True
            except ImportError:
                pdf_merger_available = False
        
        if not pdf_merger_available:
            print("Warning: PyPDF2 or pypdf not available. Trying alternative method...")
            return combine_currentscape_pdfs_matplotlib(soma_pdf_pattern, axon_pdf_pattern, 
                                                      output_filename, plot_folder, title_prefix)
        
        # Find the PDF files
        soma_files = glob.glob(os.path.join(plot_folder, soma_pdf_pattern))
        axon_files = glob.glob(os.path.join(plot_folder, axon_pdf_pattern))
        
        if not soma_files:
            print(f"Warning: No soma currentscape files found matching pattern: {soma_pdf_pattern}")
            return None
            
        if not axon_files:
            print(f"Warning: No axon currentscape files found matching pattern: {axon_pdf_pattern}")
            return None
        
        # Use the first matching file for each
        soma_file = soma_files[0]
        axon_file = axon_files[0]
        
        print(f"Combining currentscape PDFs:")
        print(f"  Soma: {soma_file}")
        print(f"  Axon: {axon_file}")
        
        # Create the merger
        merger = PdfMerger()
        
        # Add the PDFs
        merger.append(soma_file)
        merger.append(axon_file)
        
        # Create output path
        output_path = os.path.join(plot_folder, output_filename)
        
        # Write the combined PDF
        with open(output_path, 'wb') as output_file:
            merger.write(output_file)
        
        merger.close()
        
        print(f"Combined currentscape PDFs saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error combining PDFs with PyPDF2: {e}")
        print("Trying alternative matplotlib method...")
        return combine_currentscape_pdfs_matplotlib(soma_pdf_pattern, axon_pdf_pattern, 
                                                  output_filename, plot_folder, title_prefix)


def combine_currentscape_pdfs_matplotlib(soma_pdf_pattern, axon_pdf_pattern, output_filename, 
                                        plot_folder=".", title_prefix=""):
    """
    Alternative method to combine currentscape PDFs using matplotlib.
    Creates a new figure with both PDFs displayed side by side.
    
    Parameters:
    -----------
    soma_pdf_pattern : str
        File pattern or path for the soma currentscape PDF
    axon_pdf_pattern : str
        File pattern or path for the axon currentscape PDF
    output_filename : str
        Name for the combined output PDF file
    plot_folder : str, optional
        Directory containing the PDF files (default: ".")
    title_prefix : str, optional
        Prefix for the title page (default: "")
        
    Returns:
    --------
    str : Path to the combined PDF file, or None if unsuccessful
    """
    import os
    import glob
    import matplotlib.pyplot as plt
    import subprocess
    import tempfile
    
    try:
        # Find the PDF files
        soma_files = glob.glob(os.path.join(plot_folder, soma_pdf_pattern))
        axon_files = glob.glob(os.path.join(plot_folder, axon_pdf_pattern))
        
        if not soma_files or not axon_files:
            print(f"Warning: Missing currentscape files. Soma: {len(soma_files)}, Axon: {len(axon_files)}")
            return None
        
        soma_file = soma_files[0]
        axon_file = axon_files[0]
        
        print(f"Creating combined currentscape figure:")
        print(f"  Soma: {soma_file}")
        print(f"  Axon: {axon_file}")
        
        # Create figure with side-by-side layout
        fig, (ax_soma, ax_axon) = plt.subplots(1, 2, figsize=(cm_to_in(20), cm_to_in(15)))
        
        # Function to convert PDF to image and display
        def display_pdf_in_subplot(pdf_path, ax, title):
            """Try to convert PDF to image and display in subplot"""
            try:
                # Create temporary PNG file
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    png_path = tmp_file.name
                
                # Try pdftoppm first
                try:
                    result = subprocess.run(['pdftoppm', '-png', '-singlefile', '-r', '150', 
                                           pdf_path, png_path[:-4]], 
                                          capture_output=True, timeout=30)
                    if result.returncode == 0:
                        import matplotlib.image as mpimg
                        img = mpimg.imread(png_path)
                        ax.imshow(img, aspect='auto')
                        ax.axis('off')
                        ax.set_title(title, fontsize=12, pad=10)
                        os.unlink(png_path)
                        return True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    pass
                
                # Try ImageMagick convert
                try:
                    result = subprocess.run(['convert', '-density', '150', f'{pdf_path}[0]', png_path], 
                                          capture_output=True, timeout=30)
                    if result.returncode == 0:
                        import matplotlib.image as mpimg
                        img = mpimg.imread(png_path)
                        ax.imshow(img, aspect='auto')
                        ax.axis('off')
                        ax.set_title(title, fontsize=12, pad=10)
                        os.unlink(png_path)
                        return True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    pass
                
                # Clean up temp file if conversion failed
                try:
                    os.unlink(png_path)
                except:
                    pass
                
                return False
                
            except Exception as e:
                print(f"   Error converting {pdf_path}: {e}")
                return False
        
        # Try to display the PDFs as images
        soma_success = display_pdf_in_subplot(soma_file, ax_soma, 'Soma Currentscape')
        axon_success = display_pdf_in_subplot(axon_file, ax_axon, 'Axon (AIS) Currentscape')
        
        # If image conversion failed, show informative text
        if not soma_success:
            ax_soma.text(0.5, 0.7, 'SOMA CURRENTSCAPE', 
                        ha='center', va='center', transform=ax_soma.transAxes, 
                        fontsize=16, weight='bold', color='darkblue')
            ax_soma.text(0.5, 0.5, f'PDF File: {os.path.basename(soma_file)}', 
                        ha='center', va='center', transform=ax_soma.transAxes, fontsize=12)
            ax_soma.text(0.5, 0.3, 'Could not display PDF image\n(PDF conversion tools unavailable)', 
                        ha='center', va='center', transform=ax_soma.transAxes, 
                        fontsize=10, style='italic', color='gray')
            ax_soma.axis('off')
            ax_soma.set_title('Soma Currentscape', fontsize=12, pad=10)
        
        if not axon_success:
            ax_axon.text(0.5, 0.7, 'AXON CURRENTSCAPE', 
                        ha='center', va='center', transform=ax_axon.transAxes, 
                        fontsize=16, weight='bold', color='darkred')
            ax_axon.text(0.5, 0.5, f'PDF File: {os.path.basename(axon_file)}', 
                        ha='center', va='center', transform=ax_axon.transAxes, fontsize=12)
            ax_axon.text(0.5, 0.3, 'Could not display PDF image\n(PDF conversion tools unavailable)', 
                        ha='center', va='center', transform=ax_axon.transAxes, 
                        fontsize=10, style='italic', color='gray')
            ax_axon.axis('off')
            ax_axon.set_title('Axon (AIS) Currentscape', fontsize=12, pad=10)
        
        # Add overall title
        title = f'{title_prefix}Combined Currentscape Analysis' if title_prefix else 'Combined Currentscape Analysis'
        fig.suptitle(title, fontsize=16, y=0.95)
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.92])
        
        # Save the combined figure
        output_path = os.path.join(plot_folder, output_filename)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"Combined currentscape figure saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error creating combined currentscape figure: {e}")
        return None


def generate_and_combine_currentscapes(model, stim_amp=0.05, plot_fn_base='currentscape_analysis',
                                     soma_config=None, axon_config=None, 
                                     stim_dur=600, plot_folder=None):
    """
    Generate both soma and axon currentscape plots and combine them into a single PDF.
    
    Parameters:
    -----------
    model : NeuronModel instance
        The neuron model to analyze
    stim_amp : float, optional
        Current amplitude for currentscape analysis (default: 0.05)
    plot_fn_base : str, optional
        Base filename for the plots (default: 'currentscape_analysis')
    soma_config : dict, optional
        Configuration for soma currentscape plot
    axon_config : dict, optional
        Configuration for axon currentscape plot
    stim_dur : float, optional
        Stimulus duration in ms (default: 600)
    plot_folder : str, optional
        Directory for saving plots (uses model.plot_folder if available)
        
    Returns:
    --------
    dict : Results containing paths to individual and combined files
    """
    
    # Clear any existing figures to prevent memory leaks
    plt.close('all')
    
    # Set default configurations
    if soma_config is None:
        soma_config = {
            'section': 'soma',
            'segment': 0.5,
            'section_num': 0,
            'currents': ['na12.ina_ina', 'na12mut.ina_ina', 'na16.ina_ina', 'na16mut.ina_ina',
                        'ica_Ca_HVA', 'ica_Ca_LVAst', 'ihcn_Ih', 'ik_SK_E2', 'ik_SKv3_1'],
            'current_names': ['Na12', 'Na12_Mut', 'Na16', 'Na16_Mut', 'Ca_HVA', 'Ca_LVA', 'Ih', 'SK_E2', 'SKv3_1'],
            'ionic_concentrations': ["cai", "ki", "nai"]
        }
    
    if axon_config is None:
        axon_config = {
            'section': 'axon',
            'segment': 0.1,  # AIS region
            'section_num': 0,
            'currents': ['na12.ina_ina', 'na12mut.ina_ina', 'na16.ina_ina', 'na16mut.ina_ina',
                        'ica_Ca_HVA', 'ica_Ca_LVAst', 'ik_SK_E2', 'ik_SKv3_1'],  # No Ih in axon typically
            'current_names': ['Na12', 'Na12_Mut', 'Na16', 'Na16_Mut', 'Ca_HVA', 'Ca_LVA', 'SK_E2', 'SKv3_1'],
            'ionic_concentrations': ["cai", "ki", "nai"]
        }
    
    if plot_folder is None:
        plot_folder = getattr(model, 'plot_folder', '.')
    
    results = {
        'soma_success': False,
        'axon_success': False,
        'soma_file': None,
        'axon_file': None,
        'combined_file': None,
        'errors': []
    }
    
    print(f"Generating currentscape analysis for stimulus {stim_amp} nA...")
    
    # Generate soma currentscape
    try:
        print("  Generating soma currentscape...")
        model.make_currentscape_plot(
            amp=stim_amp,
            time1=0, time2=250,
            stim_start=100,
            sweep_len=300,
            pfx=f'{plot_fn_base}_soma',
            sim_config=soma_config
        )
        results['soma_success'] = True
        results['soma_file'] = f'{plot_fn_base}_soma*.pdf'
        print("  ✓ Soma currentscape generated successfully")
        
    except Exception as e:
        error_msg = f"Error generating soma currentscape: {e}"
        print(f"  ✗ {error_msg}")
        results['errors'].append(error_msg)
    
    # Generate axon currentscape
    try:
        print("  Generating axon currentscape...")
        model.make_currentscape_plot(
            amp=stim_amp,
            time1=0, time2=250,
            stim_start=100,
            sweep_len=300,
            pfx=f'{plot_fn_base}_axon',
            sim_config=axon_config
        )
        results['axon_success'] = True
        results['axon_file'] = f'{plot_fn_base}_axon*.pdf'
        print("  ✓ Axon currentscape generated successfully")
        
    except Exception as e:
        error_msg = f"Error generating axon currentscape: {e}"
        print(f"  ✗ {error_msg}")
        results['errors'].append(error_msg)
    
    # Combine the PDFs if both were successful
    if results['soma_success'] and results['axon_success']:
        print("  Combining currentscape PDFs...")
        try:
            # Find the actual currentscape files that were generated
            soma_files = glob.glob(os.path.join(plot_folder, results['soma_file']))
            axon_files = glob.glob(os.path.join(plot_folder, results['axon_file']))
            
            print(f"    Found soma files: {soma_files}")
            print(f"    Found axon files: {axon_files}")
            
            if not soma_files:
                error_msg = f"No soma currentscape files found matching pattern: {results['soma_file']}"
                print(f"  ✗ {error_msg}")
                results['errors'].append(error_msg)
                return results
                
            if not axon_files:
                error_msg = f"No axon currentscape files found matching pattern: {results['axon_file']}"
                print(f"  ✗ {error_msg}")
                results['errors'].append(error_msg)
                return results
            
            combined_path = combine_currentscape_pdfs(
                soma_pdf_pattern=results['soma_file'],
                axon_pdf_pattern=results['axon_file'],
                output_filename=f'{plot_fn_base}_combined.pdf',
                plot_folder=plot_folder,
                title_prefix=f'{plot_fn_base.replace("_", " ").title()}: '
            )
            
            if combined_path:
                # Make sure we have the absolute path
                if not os.path.isabs(combined_path):
                    combined_path = os.path.abspath(combined_path)
                results['combined_file'] = combined_path
                print(f"  ✓ Combined currentscape saved to: {combined_path}")
                
                # Verify the file exists
                if os.path.exists(combined_path):
                    file_size = os.path.getsize(combined_path)
                    print(f"    File size: {file_size} bytes")
                else:
                    error_msg = f"Combined currentscape file not found after creation: {combined_path}"
                    print(f"  ✗ {error_msg}")
                    results['errors'].append(error_msg)
            else:
                error_msg = "Failed to combine currentscape PDFs"
                print(f"  ✗ {error_msg}")
                results['errors'].append(error_msg)
                
        except Exception as e:
            error_msg = f"Error combining currentscape PDFs: {e}"
            print(f"  ✗ {error_msg}")
            results['errors'].append(error_msg)
    else:
        error_msg = "Cannot combine PDFs - one or both currentscape generations failed"
        print(f"  ✗ {error_msg}")
        results['errors'].append(error_msg)
    
    return results
    
def create_complete_analysis(model, stim_amps=None, single_stim_amp=0.05, dt=0.1, 
                           plot_fn_base='complete_analysis', rec_extra=False, 
                           stim_dur=600, v_time=550, clr='cadetblue',
                           soma_config=None, axon_config=None, save_individual=True):
    """
    Create a complete neuron analysis combining comprehensive plots and currentscapes.
    This is a one-stop function that generates:
    1. Comprehensive analysis (input resistance + dV/dt)
    2. Combined currentscape plots (soma + axon)
    3. Final PDF with everything combined
    
    Parameters:
    -----------
    model : NeuronModel instance
        The neuron model to analyze
    stim_amps : list, optional
        Current amplitudes for input resistance analysis
    single_stim_amp : float, optional
        Single current amplitude for dV/dt and currentscape analysis (default: 0.05)
    dt : float, optional
        Time step for simulation (default: 0.1)
    plot_fn_base : str, optional
        Base filename for all plots (default: 'complete_analysis')
    rec_extra : bool, optional
        Whether to record extra locations (default: False)
    stim_dur : float, optional
        Stimulus duration in ms (default: 600)
    v_time : float, optional
        Time point for voltage measurements in ms (default: 550)
    clr : str, optional
        Color for single trace plots (default: 'cadetblue')
    soma_config : dict, optional
        Configuration for soma currentscape plot
    axon_config : dict, optional
        Configuration for axon currentscape plot
    save_individual : bool, optional
        Whether to save individual component plots (default: True)
        
    Returns:
    --------
    dict : Complete results including all generated files and analysis data
    """
    
    # Clear all existing figures at the start to prevent memory leaks
    plt.close('all')
    
    # Set matplotlib to limit the number of figures to prevent memory issues
    import matplotlib as mpl
    mpl.rcParams['figure.max_open_warning'] = 10  # Warn after 10 figures instead of 20
    
    print(f"Starting complete neuron analysis...")
    print("="*60)
    
    results = {
        'comprehensive_analysis': None,
        'currentscape_analysis': None,
        'final_combined_pdf': None,
        'success': False,
        'errors': []
    }
    
    # Step 1: Generate comprehensive analysis (input resistance + dV/dt)
    print("Step 1: Generating comprehensive analysis...")
    try:
        fig, comprehensive_results = plot_comprehensive_analysis(
            model=model,
            stim_amps=stim_amps,
            single_stim_amp=single_stim_amp,
            dt=dt,
            plot_fn=plot_fn_base,  # Don't add '_comprehensive' here
            rec_extra=rec_extra,
            stim_dur=stim_dur,
            v_time=v_time,
            clr=clr,
            save_individual=save_individual
        )
        
        results['comprehensive_analysis'] = comprehensive_results
        # The actual file path where the comprehensive PDF is saved
        comprehensive_pdf = f'{model.plot_folder if hasattr(model, "plot_folder") else "."}/{plot_fn_base}_comprehensive.pdf'
        
        # Close the figure to free memory
        plt.close(fig)
        
        print(f"  Expected comprehensive PDF path: {comprehensive_pdf}")
        print(f"  File exists: {os.path.exists(comprehensive_pdf)}")
        if os.path.exists(comprehensive_pdf):
            print(f"  File size: {os.path.getsize(comprehensive_pdf)} bytes")
        
        print(f"✓ Comprehensive analysis completed")
        if 'input_resistance' in comprehensive_results:
            mean_rin = comprehensive_results['input_resistance'].get('mean_resistance', 'N/A')
            print(f"  Mean input resistance: {mean_rin} MΩ")
        if 'dvdt_analysis' in comprehensive_results:
            num_spikes = comprehensive_results['dvdt_analysis'].get('num_spikes', 'N/A')
            max_dvdt = comprehensive_results['dvdt_analysis'].get('max_dvdt', 'N/A')
            print(f"  Number of spikes: {num_spikes}")
            print(f"  Max dV/dt: {max_dvdt:.1f} mV/ms" if isinstance(max_dvdt, (int, float)) else f"  Max dV/dt: {max_dvdt}")
        
    except Exception as e:
        error_msg = f"Error in comprehensive analysis: {e}"
        print(f"✗ {error_msg}")
        results['errors'].append(error_msg)
        return results
    
    # Step 2: Generate and combine currentscape plots
    print("\nStep 2: Generating combined currentscape analysis...")
    try:
        currentscape_results = generate_and_combine_currentscapes(
            model=model,
            stim_amp=single_stim_amp,
            plot_fn_base=f'{plot_fn_base}_currentscape',
            soma_config=soma_config,
            axon_config=axon_config,
            stim_dur=stim_dur
        )
        
        results['currentscape_analysis'] = currentscape_results
        
        if currentscape_results['combined_file']:
            print(f"✓ Combined currentscape analysis completed")
        else:
            error_msg = f"Currentscape combination failed: {currentscape_results['errors']}"
            print(f"✗ {error_msg}")
            results['errors'].append(error_msg)
            return results
            
    except Exception as e:
        error_msg = f"Error in currentscape analysis: {e}"
        print(f"✗ {error_msg}")
        results['errors'].append(error_msg)
        return results
    
    # Step 3: Combine everything into final PDF
    print("\nStep 3: Creating final combined PDF...")
    try:
        # Debug: check what we have from previous steps
        print(f"  Comprehensive PDF: {comprehensive_pdf}")
        print(f"  Currentscape results: {currentscape_results}")
        
        if currentscape_results['combined_file'] is None:
            error_msg = "No combined currentscape file available"
            print(f"✗ {error_msg}")
            results['errors'].append(error_msg)
            return results
        
        # Check if files exist before trying to combine
        if not os.path.exists(comprehensive_pdf):
            error_msg = f"Comprehensive PDF not found: {comprehensive_pdf}"
            print(f"✗ {error_msg}")
            results['errors'].append(error_msg)
            return results
            
        if not os.path.exists(currentscape_results['combined_file']):
            error_msg = f"Combined currentscape PDF not found: {currentscape_results['combined_file']}"
            print(f"✗ {error_msg}")
            results['errors'].append(error_msg)
            return results
        
        print(f"  ✓ Both input files found")
        
        final_pdf = append_currentscapes_to_comprehensive(
            comprehensive_pdf_path=comprehensive_pdf,
            currentscape_pdf_path=currentscape_results['combined_file'],
            output_filename=f'{model.plot_folder if hasattr(model, "plot_folder") else "."}/{plot_fn_base}_COMPLETE.pdf'
        )
        
        if final_pdf:
            results['final_combined_pdf'] = final_pdf
            results['success'] = True
            print(f"✓ Complete analysis PDF created successfully")
            print(f"  Final file: {final_pdf}")
        else:
            error_msg = "Failed to create final combined PDF"
            print(f"✗ {error_msg}")
            results['errors'].append(error_msg)
            
    except Exception as e:
        error_msg = f"Error creating final combined PDF: {e}"
        print(f"✗ {error_msg}")
        results['errors'].append(error_msg)
        import traceback
        traceback.print_exc()
    
    print("="*60)
    print(f"Complete analysis {'completed successfully' if results['success'] else 'failed'}")
    
    return results

def append_currentscapes_to_comprehensive(comprehensive_pdf_path, currentscape_pdf_path, 
                                        output_filename=None):
    """
    Append the combined currentscape PDF to the comprehensive analysis PDF.
    
    Parameters:
    -----------
    comprehensive_pdf_path : str
        Path to the comprehensive analysis PDF
    currentscape_pdf_path : str
        Path to the combined currentscape PDF
    output_filename : str, optional
        Name for the final combined PDF. If None, will use comprehensive_pdf_path with '_with_currentscapes' suffix
        
    Returns:
    --------
    str : Path to the final combined PDF, or None if unsuccessful
    """
    
    try:
        print(f"DEBUG: Starting PDF merge...")
        print(f"  Comprehensive PDF: {comprehensive_pdf_path}")
        print(f"  Currentscape PDF: {currentscape_pdf_path}")
        print(f"  Output filename: {output_filename}")
        
        # Try using PyPDF2 first
        pdf_merger_available = False
        merger_type = None
        
        try:
            from PyPDF2 import PdfMerger
            pdf_merger_available = True
            merger_type = "PyPDF2"
            print("  Using PyPDF2 for PDF merging")
        except ImportError:
            try:
                from pypdf import PdfMerger
                pdf_merger_available = True
                merger_type = "pypdf"
                print("  Using pypdf for PDF merging")
            except ImportError:
                print("  No PDF merger library available")
        
        # If no PDF merger, try system commands
        if not pdf_merger_available:
            print("  Trying system command fallback...")
            return merge_pdfs_with_system_command(comprehensive_pdf_path, currentscape_pdf_path, output_filename)
        
        # Check if files exist
        if not os.path.exists(comprehensive_pdf_path):
            print(f"Error: Comprehensive PDF not found: {comprehensive_pdf_path}")
            return None
            
        if not os.path.exists(currentscape_pdf_path):
            print(f"Error: Currentscape PDF not found: {currentscape_pdf_path}")
            return None
        
        print(f"  Both input files exist ✓")
        
        # Create output filename if not provided
        if output_filename is None:
            base_name = os.path.splitext(comprehensive_pdf_path)[0]
            output_filename = f"{base_name}_with_currentscapes.pdf"
        elif not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        print(f"Combining PDFs using {merger_type}:")
        print(f"  Comprehensive: {comprehensive_pdf_path}")
        print(f"  Currentscapes: {currentscape_pdf_path}")
        print(f"  Output: {output_filename}")
        
        # Create the merger
        merger = PdfMerger()
        
        # Add the comprehensive analysis first
        print("  Adding comprehensive PDF...")
        merger.append(comprehensive_pdf_path)
        
        # Add the currentscape analysis
        print("  Adding currentscape PDF...")
        merger.append(currentscape_pdf_path)
        
        # Write the combined PDF
        print("  Writing combined PDF...")
        with open(output_filename, 'wb') as output_file:
            merger.write(output_file)
        
        merger.close()
        
        # Verify the output file was created
        if os.path.exists(output_filename):
            file_size = os.path.getsize(output_filename)
            print(f"✓ Complete analysis PDF saved to: {output_filename}")
            print(f"  File size: {file_size} bytes")
            return output_filename
        else:
            print(f"Error: Output file was not created: {output_filename}")
            return None
        
    except Exception as e:
        print(f"Error combining comprehensive and currentscape PDFs: {e}")
        import traceback
        traceback.print_exc()
        return None


def merge_pdfs_with_system_command(pdf1_path, pdf2_path, output_filename):
    """
    Fallback method to merge PDFs using system commands when PyPDF2/pypdf aren't available.
    """
    try:
        print("  Attempting PDF merge with system commands...")
        
        # Create output filename if not provided
        if output_filename is None:
            base_name = os.path.splitext(pdf1_path)[0]
            output_filename = f"{base_name}_with_currentscapes.pdf"
        elif not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        # Try pdftk first (most reliable)
        try:
            result = subprocess.run(['pdftk', pdf1_path, pdf2_path, 'cat', 'output', output_filename], 
                                  capture_output=True, timeout=60)
            if result.returncode == 0 and os.path.exists(output_filename):
                print(f"  ✓ PDFs merged using pdftk: {output_filename}")
                return output_filename
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("  pdftk not available or timeout")
        
        # Try ghostscript
        try:
            result = subprocess.run(['gs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', 
                                   f'-sOutputFile={output_filename}', pdf1_path, pdf2_path], 
                                  capture_output=True, timeout=60)
            if result.returncode == 0 and os.path.exists(output_filename):
                print(f"  ✓ PDFs merged using ghostscript: {output_filename}")
                return output_filename
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("  ghostscript not available or timeout")
        
        # If system commands fail, create a simple combined PDF using matplotlib
        print("  Creating combined PDF using matplotlib...")
        return create_combined_pdf_with_matplotlib(pdf1_path, pdf2_path, output_filename)
        
    except Exception as e:
        print(f"Error in system command PDF merge: {e}")
        return None


def create_combined_pdf_with_matplotlib(pdf1_path, pdf2_path, output_filename):
    """
    Create a combined PDF by displaying both PDFs as images in a matplotlib figure.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        
        # Create a new PDF with matplotlib
        with PdfPages(output_filename) as pdf:
            # Add a title page
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.text(0.5, 0.8, 'COMBINED NEURON ANALYSIS', 
                   ha='center', va='center', fontsize=24, weight='bold')
            ax.text(0.5, 0.6, 'Comprehensive Analysis + Currentscapes', 
                   ha='center', va='center', fontsize=16)
            ax.text(0.5, 0.4, f'Comprehensive: {os.path.basename(pdf1_path)}', 
                   ha='center', va='center', fontsize=12)
            ax.text(0.5, 0.3, f'Currentscapes: {os.path.basename(pdf2_path)}', 
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            
            # Add note about original files
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.text(0.5, 0.5, 'NOTE: PDF merging libraries not available.\n\n'
                              'The original analysis files are:\n\n'
                              f'1. Comprehensive Analysis:\n   {pdf1_path}\n\n'
                              f'2. Combined Currentscapes:\n   {pdf2_path}\n\n'
                              'Please view these files separately for complete analysis.',
                   ha='center', va='center', fontsize=12, 
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray"))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
        
        if os.path.exists(output_filename):
            print(f"  ✓ Combined PDF created (with file references): {output_filename}")
            return output_filename
        else:
            print(f"  ✗ Failed to create combined PDF: {output_filename}")
            return None
            
    except Exception as e:
        print(f"Error creating combined PDF with matplotlib: {e}")
        return None

from NaMut import *
import NrnHelper as nhlpr
        
def plot_mut(mut_name):
    #initialize WT and stuff
    dt = 0.005
    sim = NaMut(mut_name)
    sim.make_wt()
    #plot volts and dvdt same figure
    fig_volts,axs_volts = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
    sim.plot_stim(axs = axs_volts[0],dt=dt,stim_amp = 0.3,rec_extra = True)
    #updating the sim (NaMut) to update hold the simulation so we won't need to redo it.
    sim.volt_soma_wt = sim.volt_soma 
    sim.I_wt = sim.I
    sim.extra_vms_wt = sim.extra_vms
    nhlpr.plot_dvdt_from_volts(sim.volt_soma_wt,dt = dt,skip_first = True,axs=axs_volts[1])
    fig_extra_vs,extra_vs_axs = plt.subplots(3,figsize=(cm_to_in(8),cm_to_in(23)))
    plot_extra_volts(sim.t,sim.extra_vms_wt,axs =extra_vs_axs)

    sim.make_het()
    sim.plot_stim(axs = axs_volts[0],dt=dt,stim_amp = 0.3,rec_extra = True,clr = 'red')
    nhlpr.plot_dvdt_from_volts(sim.volt_soma,dt = dt,skip_first = True,axs=axs_volts[1],clr = 'red')
    plot_extra_volts(sim.t,sim.extra_vms,axs =extra_vs_axs ,clr = 'red')

    fig_volts.savefig(f'{sim.plot_folder}{mut_name}_Vs_dvdt.pdf')
    fig_extra_vs.savefig(f'{sim.plot_folder}{mut_name}_ext_Vs.pdf')
plot_mut('A1773T')
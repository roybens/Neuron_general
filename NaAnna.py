from NeuronModelClass import NeuronModel
from NrnHelper import *
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import numpy as np
class NaAnna:
    def __init__(self,na12name = 'na12_anna', na12mechs = ['na12','na12mut'],na16name = 'na16_anna', na16mechs = ['na16','na16mut'], params_folder = './params/',nav12=1.2,nav16=1.4,plots_folder = f'./Plots/'):
        self.l5mdl = NeuronModel(nav12=nav12, nav16=nav16)
        #mechs = ['na12']
        #update_mod_param(self.l5mdl, mechs, 2, gbar_name='gbar')
        #mechs = ['na12mut']
        #update_mod_param(self.l5mdl, mechs, 0, gbar_name='gbar')
        self.na12mechs = na12mechs
        self.na16mechs = na16mechs
        self.plot_folder = plots_folder 
        print(f'using na12_file {na12name}')
        p_fn_na12 = f'{params_folder}{na12name}.txt'
        self.na12_p = update_mech_from_dict(self.l5mdl, p_fn_na12, self.na12mechs) 
        print(f'using na16_file {na16name}')
        self.plot_folder = f'{plots_folder}Anna/'
        Path(self.plot_folder).mkdir(parents=True, exist_ok=True)
        p_fn_na16 = f'{params_folder}{na16name}.txt'
        self.na16_p = update_mech_from_dict(self.l5mdl, p_fn_na16, self.na16mechs) 

    def update_gfactor(self,gbar_factor = 1):
        update_mod_param(self.l5mdl, self.mut_mech, gbar_factor, gbar_name='gbar')

    def plot_stim(self,stim_amp = 0.3,dt = 0.01,clr = 'black',plot_fn = 'step',axs = None,rec_extra = False):
        self.dt = dt
        if not axs:
            fig,axs = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        self.l5mdl.init_stim(amp=stim_amp)
        if rec_extra:
            Vm, I, t, stim,extra_vms = self.l5mdl.run_model(dt=dt,rec_extra = rec_extra)
            self.extra_vms = extra_vms
        else:
            Vm, I, t, stim = self.l5mdl.run_model(dt=dt)
            
        self.volt_soma = Vm
        self.I = I
        self.t = t
        self.stim = stim
        
        axs.plot(t,Vm, label='Vm', color=clr,linewidth=1)
        axs.locator_params(axis='x', nbins=5)
        axs.locator_params(axis='y', nbins=8)
        #plt.show()
        #add_scalebar(axs)
        file_path_to_save=f'{self.plot_folder}Anna_{plot_fn}.pdf'
        fig.savefig(file_path_to_save, format='pdf', dpi=my_dpi, bbox_inches="tight")
        return axs

    def plot_currents(self,stim_amp = 0.3,dt = 0.01,clr = 'black',plot_fn = 'step',axs = None):
        if not axs:
            fig,axs = plt.subplots(4,figsize=(cm_to_in(8),cm_to_in(30)))
        self.l5mdl.init_stim(amp=stim_amp)
        Vm, I, t, stim = self.l5mdl.run_model(dt=dt)
        axs[0].plot(t,Vm, label='Vm', color=clr,linewidth=1)
        axs[0].locator_params(axis='x', nbins=5)
        axs[0].locator_params(axis='y', nbins=8)
        
        axs[1].plot(t,I['Na'],label = 'Na',color = 'red')
        axs[2].plot(t,I['K'],label = 'K',color = 'black')
        axs[3].plot(t,I['Ca'],label = 'Ca',color = 'green')
        #add_scalebar(axs)
        file_path_to_save=f'{self.plot_folder}AnnaModel_{plot_fn}.pdf'
        plt.savefig(file_path_to_save+'.pdf', format='pdf', dpi=my_dpi, bbox_inches="tight")
        return axs


        
    def plot_fi_curve(self,start,end,nruns,wt_data = None,ax1 = None, fig = None,fn = 'ficurve'):
        fis = get_fi_curve(self.l5mdl,start,end,nruns,dt = 0.1,wt_data = wt_data,ax1=ax1,fig=fig,fn=f'{self.plot_folder}{fn}.pdf')
        return fis
    

    def plot_volts_dvdt(self,stim_amp = 0.3):
        fig_volts,axs_volts = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        fig_dvdt,axs_dvdt = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        self.plot_stim(axs = axs_volts,dt=0.005)
        plot_dvdt_from_volts(self.volt_soma,self.dt,axs_dvdt)
        file_path_to_save=f'{self.plot_folder}AnnaModel_volts_dvdt_{stim_amp}.pdf'
        fig_dvdt.savefig(file_path_to_save, format='pdf', dpi=my_dpi, bbox_inches="tight")
        file_path_to_save=f'{self.plot_folder}AnnaModel_volts_{stim_amp}.pdf'
        fig_volts.savefig(file_path_to_save, format='pdf', dpi=my_dpi, bbox_inches="tight")

    

    
    

sim = NaAnna()
sim.plot_volts_dvdt()
sim.plot_fi_curve(0,1,6)
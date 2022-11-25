from NeuronModelClass import NeuronModel
from NrnHelper import *
import matplotlib.pyplot as plt
import sys
class NaMut:
    def __init__(self,mut_name = None,wt_file = 'na12WT', wt_mec = 'na12',mut_mec = 'na12mut', params_folder = './params/')
    self.l5mdl = NeuronModel()
    self.mut_mech = mut_mec
    self.wt_mech = wt_mec
    self.plot_folder = f'./Plots/'
    if wt_file:
        p_fn = f'{params_folder}{wt_file}.txt'
        self.wt_p = update_mech_from_dict(self.l5mdl, p_fn, self.wt_mech) 
    if mut_name:
        self.mut_name = mut_name
        self.plot_folder = f'./Plots/{self.mut_name}/'
        Path(self.plot_folder).mkdir(parents=True, exist_ok=True)
        p_fn = f'{params_folder}{self.mut_name}.txt'
        self.mut_p = update_mech_from_dict(self.l5mdl, p_fn, self.mut_mech) 
    

    def update_model(self):
        l5mdl.h.working()
        #updating the WT 
        update_mech_from_dict(self.l5mdl, self.wt_p, self.wt_mech,input_dict = True)
        #updating the Mut 
        update_mech_from_dict(self.l5mdl, self.mut_p, self.mut_mech,input_dict = True)

    def plot_stim(self,stim_amp = 0.5,clr = 'black',plot_fn = 'step'):
        l5mdl.init_stim(amp=stim_amp)
        Vm, I, t, stim = l5mdl.run_model(dt=0.01)
        plot_stim_volts_pair(Vm, 'Step Stim 500pA', file_path_to_save='{self.plot_folder}{self.mut_name}_{plot_fn}.pdf', times=t,color_str=clr)

    def plot_fi_curve(self,start,end,nruns,wt_data = None,ax1 = None, fig = None,fn = 'ficurve'):
        fis = get_fi_curve(self.l5mdl,start,end,nruns,dt = 0.1,wt_data = wt_data,ax1=ax1,fig=fig,fn=f'{self.plot_folder}{fn}.pdf')
        return fis

    def update_gfactor(self,gbar_factor = 1):
        update_mod_param(self.l5mdl, self.mut_mech, gbar_factor, gbar_name='gbar')

"""
    def make_hmm_cultured_wt(gbar_factor = 1):
        #fig, ficurveax = plt.subplots(1, 1)
        l5mdl.h.working()
        mechs = ['na16']
        dict_fn_wt = f'{params_folder}/na16WT.txt'
        update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
        update_mod_param(l5mdl, mechs, 3, gbar_name='gbar')
        mechs = ['na16mut']
        dict_fn_mut = f'{params_folder}/na16Mut.txt'
        update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
        update_mod_param(l5mdl, mechs, 0, gbar_name='gbar')
        if gbar_factor != 1:
            update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')

    def make_hmm_cultured_mut(gbar_factor = 1):
        #fig, ficurveax = plt.subplots(1, 1)
        l5mdl.h.working()
        mechs = ['na16']
        dict_fn_wt = f'{params_folder}/na16WT.txt'
        update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
        update_mod_param(l5mdl, mechs, 2, gbar_name='gbar')
        mechs = ['na16mut']
        dict_fn_mut = f'{params_folder}/na16Mut.txt'
        update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
        update_mod_param(l5mdl, mechs, 1, gbar_name='gbar')
        if gbar_factor != 1:
            update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')

    def make_hmm_cultured_wt_TTX(gbar_factor = 1):
        #fig, ficurveax = plt.subplots(1, 1)
        l5mdl.h.working()
        mechs = ['na16']
        dict_fn_wt = f'{params_folder}/na16WT.txt'
        update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
        update_mod_param(l5mdl, mechs,1, gbar_name='gbar')
        mechs = ['na16mut']
        dict_fn_mut = f'{params_folder}/na16Mut.txt'
        update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
        update_mod_param(l5mdl, mechs, 0, gbar_name='gbar')
        if gbar_factor != 1:
            update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')

    def make_hmm_cultured_mut_TTX(gbar_factor = 1):
        #fig, ficurveax = plt.subplots(1, 1)
        l5mdl.h.working()
        mechs = ['na16']
        dict_fn_wt = f'{params_folder}/na16WT.txt'
        update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
        update_mod_param(l5mdl, mechs, 0, gbar_name='gbar')
        mechs = ['na16mut']
        dict_fn_mut = f'{params_folder}/na16Mut.txt'
        update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
        update_mod_param(l5mdl, mechs, 1, gbar_name='gbar')
        if gbar_factor != 1:
            update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')
"""

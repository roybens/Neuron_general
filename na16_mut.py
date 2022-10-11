from NeuronModelClass import NeuronModel
from NrnHelper import *
import matplotlib.pyplot as plt


params_folder = './params'

def make_hmm_wt():
    l5mdl = NeuronModel()
    dict_fn = f'{params_folder}/na16WT.txt'
    update_mech_from_dict(l5mdl, dict_fn, mechs)
    fig, ficurveax = plt.subplots(1, 1)
    l5mdl.h.working()
    mechs = ['na16']
    dict_fn = f'{params_folder}/na16WT.txt'
    update_mech_from_dict(l5mdl, dict_fn, mechs)
    mechs = ['na16mut']
    update_mech_from_dict(l5mdl, dict_fn, mechs)
    l5mdl.init_stim(amp=0.5)
    Vm, I, t, stim = l5mdl.run_model(dt=0.01)
    plot_stim_volts_pair(Vm, 'Step Stim 500pA', file_path_to_save='./Plots/WT_500pA', times=t)
    fig2, I_axs = plt.subplots(1, 1)
    I_axs.plot(t, I['Na'], label='Na', color='blue')
    I_axs.plot(t, I['Ca'], label='Ca', color='red')
    I_axs.plot(t, I['K'], label='Ca', color='green')
    I_axs.legend()
    fig2.savefig('./Plots/WT_Na16_Is.pdf')
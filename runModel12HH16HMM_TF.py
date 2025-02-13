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
import matplotlib.pyplot as plt
import numpy as np
import NrnHelper as NH
#import Na12ModelGY as Mature
from na12HH16HMM_TF import *
import na12HH16HMM_TF as tf
import os


#_____________For Looping through mutants________________________________________________________________________
# for i in range(1,13):
#         for j in range(1,5):
#             mutant = 'mut'+str(i)+'_'+str(j)
#             #mutant = 'test0921'
#             # path = os.path.join(root_path, mutant)
#             # os.mkdir(path)
#             #sim = tf.na12HH16HMM_TF(na12name = 'na12_TF2' , mut_name = 'na12_TF2', na16name = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/{mutant}/')
#             sim = tf.na12HH16HMM_TF(na16name = f'{mutant}_Na16hof',na16mut = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/synth_na16muts_HOMtest/scank/{mutant}/')

#             #sim = tf.na12HH16HMM_TF(na16name = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/{mutant}/')
#             sim_config = {
#                             'section' : 'soma',
#                             'segment' : 0.5,
#                             'section_num': 0,
#                             #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'],
#                             'currents' : ['ina','ica','ik'],
#                             'ionic_concentrations' :["cai", "ki", "nai"]
                            
#                         }
#             current_names = sim_config['currents']
#             Vm, I, t, stim, ionic = sim.make_current_scape(sim_config=sim_config)

#             plot_config = {
#                     "output": {
#                         "savefig": True,
#                         "dir": "./Plots/Currentscape/TEST/",
#                         "fname": "test_plot",
#                         "extension": "pdf",
#                         "dpi": 600,
#                         "transparent": False
#                     },
#                     "current": {"names": current_names},
#                     "ions":{"names": ["ca", "k", "na"]},
#                     "voltage": {"ylim": [-90, 50]},
#                     "legendtextsize": 5,
#                     "adjust": {
#                         "left": 0.15,
#                         "right": 0.8,
#                         "top": 1.0,
#                         "bottom": 0.0
#                         }
#                     }
#             #print(I.keys())
#             #sim.make_current_scape()
#             #sim.plot_stim()
#             # sim.plot_currents()
#             # sim.plot_volts_dvdt()
#             # sim.plot_fi_curve(0,5,20,fn = f'16HMM_muts_TF')
#             #sim.get_axonal_ks()
#             #sim.plot_axonal_ks()

#             #scan12_16(na16name = f'{mutant}_Na16hof',na16mut = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/synth_na16muts_HOMtest/{mutant}/')
#             scanK(na16name = f'{mutant}_Na16hof',na16mut = f'{mutant}_Na16hof', plots_folder = f'./Plots/12HH16HMM_TF/synth_na16muts_HOMtest/{mutant}/')
            
#             #dvdt_all_plot()
#             #print(h.cell.soma.psection())
###___________________________________________________________________________________________________________


#mutant = 'mut'+str(i)+'_'+str(j)
mutant = 'mut4_4_100523'

#sim = tf.na12HH16HMM_TF(na16name = 'na16mut44_092623',na16mut = 'na16mut44_092623')
sim = tf.na12HH16HMM_TF()

sim_config = {
                'section' : 'soma',
                'segment' : 0.5,
                'section_num': 0,
                #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'],
                'currents' : ['ina','ica','ik'],
                'ionic_concentrations' :["cai", "ki", "nai"]
                
            }
current_names = sim_config['currents']
Vm, I, t, stim, ionic = sim.make_current_scape(sim_config=sim_config)

plot_config = {
        "output": {
            "savefig": True,
            "dir": "./Plots/Currentscape/TEST/",
            "fname": "test_plot",
            "extension": "pdf",
            "dpi": 600,
            "transparent": False
        },
        "current": {"names": current_names},
        "ions":{"names": ["ca", "k", "na"]},
        "voltage": {"ylim": [-90, 50]},
        "legendtextsize": 5,
        "adjust": {
            "left": 0.15,
            "right": 0.8,
            "top": 1.0,
            "bottom": 0.0
            }
        }
# print('keys &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
# print(I.keys())


# print ('currentscape &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
# sim.make_current_scape()


# print ('stim &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
# sim.plot_stim()


# print ('current &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
# sim.plot_currents()


# print ('volts dvdt &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
# sim.plot_volts_dvdt()

# print ('FI curve &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
# sim.plot_fi_curve(0,5,20,fn = f'16HMM_mut44MORANmut_TF')

#sim.get_axonal_ks()
#sim.plot_axonal_ks()
# print ('scan12_16 &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
#scan12_16(na16name = 'na16MORAN_100223',na16mut = 'na16MORAN_100223', plots_folder = f'./Plots/12HH16HMM_TF/100323/{mutant}/')

#print ('scanK &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
#scanK(na16name = 'na16mut13_092623',na16mut = 'na16mut13_092623', plots_folder = f'./Plots/12HH16HMM_TF/092623/{mutant}/')

#print ('dvdt_all &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
#dvdt_all_plot() #requires hardcode changes in model to run
#print(h.cell.soma.psection())

# overexp(na16name = 'na16mut44_092623',na16mut = 'na16mut44_092623', 
#   plots_folder = f'./Plots/12HH16HMM_TF/100223/{mutant}/')
#rng = [.05,.1,.15,.2]
# rng = [.3, .4, .5, .6, .7, .8, .9, 1]
# for i in rng:
#     ttx(na16name = 'na16MORAN_100223',na16mut = 'na16MORAN_100223', 
#         plots_folder = f'./Plots/12HH16HMM_TF/100323/{mutant}/ttxWTrange5-100/', wt_factor =i, mut_factor =0,fnpre =f'mut_{i}')
# ttx(na16name = 'na16MORAN_100223',na16mut = 'na16MORAN_100223', 
#     plots_folder = f'./Plots/12HH16HMM_TF/100323/{mutant}/ttx2line1/', wt_factor =.4, mut_factor =0,fnpre ='mut_.4')

# ttx(na16name = 'na16mut44_092623',na16mut = 'na16mut44_092623', 
#     plots_folder = f'./Plots/12HH16HMM_TF/100323/{mutant}/ttx2line/', wt_factor =.4, mut_factor =0,fnpre =f'mut_.4')

####______________100423 Experiments________________________
# overexp(na16name = 'na16mut44_092623',na16mut = 'na16mut44_092623', wt_fac =2.2, mut_fac=None, 
#   plots_folder = f'./Plots/12HH16HMM_TF/100423/120WT/')
####________________________________________________________



####______________100523 Experiments________________________

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2 ,mut_fac = 0, 
#   plots_folder = f'./Plots/12HH16HMM_TF/101123/TimParamsCSVs/100WT/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2.4 ,mut_fac = 0, 
#   plots_folder = f'./Plots/12HH16HMM_TF/101123/TimParamsCSVs/120WT/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =0 ,mut_fac = 2, 
#   plots_folder = f'./Plots/12HH16HMM_TF/101123/TimParamsCSVs/100WT_test02/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2 ,mut_fac = 0.4, 
#   plots_folder = f'./Plots/12HH16HMM_TF/101123/TimParamsCSVs/100WT20G1625R/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =0.4 ,mut_fac = 0, 
#   plots_folder = f'./Plots/12HH16HMM_TF/101123/TimParamsCSVs/20WT/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =0 ,mut_fac = 0.4, 
#   plots_folder = f'./Plots/12HH16HMM_TF/101123/TimParamsCSVs/20G1625R/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =1 ,mut_fac = 1, 
#   plots_folder = f'./Plots/12HH16HMM_TF/101123/TimParamsCSVs/50WT50G1625R/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2 ,mut_fac = .4, 
#   plots_folder = f'./Plots/12HH16HMM_TF/101123/TimParamsCSVs/100WT20G1625R_v_120WT/')

#____________________________________________________________



############################################################
####______________103023 Experiments: increase Na16 by 200%________________________

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2 ,mut_fac = 0, 
#   plots_folder = f'./Plots/12HH16HMM_TF/111423noINA_INA/100WT/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2.4 ,mut_fac = 0, 
#   plots_folder = f'./Plots/12HH16HMM_TF/110623/120WT/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2 ,mut_fac = 0.8, 
#   plots_folder = f'./Plots/12HH16HMM_TF/110623/100WT20G1625R/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =0.4 ,mut_fac = 0, 
#   plots_folder = f'./Plots/12HH16HMM_TF/110623/20WT/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =0 ,mut_fac = 0.8, 
#   plots_folder = f'./Plots/12HH16HMM_TF/110623/20G1625R/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =1 ,mut_fac = 2, 
#   plots_folder = f'./Plots/12HH16HMM_TF/110623/50WT50G1625R/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2 ,mut_fac = .4, 
#   plots_folder = f'./Plots/12HH16HMM_TF/110623/100WT20G1625R_v_120WT/')


####______________111723 Experiments: Double Checking data and that wt_fac wasn't updated twice________________________

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =0.4 ,mut_fac = 0, 
#   plots_folder = f'./Plots/12HH16HMM_TF/111723/20WT/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =0 ,mut_fac = 0.4, 
#   plots_folder = f'./Plots/12HH16HMM_TF/111723/20G1625R/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =2.4 ,mut_fac = 0, 
#   plots_folder = f'./Plots/12HH16HMM_TF/111723/120WT5_removeINA_INA/')

# overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =1,mut_fac = 1, 
#   plots_folder = f'./Plots/12HH16HMM_TF/112723/HET')
# ttx(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_factor =1,mut_factor = 1, 
#   plots_folder = f'./Plots/12HH16HMM_TF/111723/base/100WT14')

# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16mut44_092623', wt_fac =2, mut_fac = 0, 
#                                amp = 1, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111723/na12mechchange',
#                                fnpre = '100WT', wtorhet = 'WT')



###______________111523 Experiments to make TTX currentscape plots______________________________
sim.make_currentscape_plot()
# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16mut44_092623', wt_fac =2, mut_fac = 0, 
#                                amp = 0.5, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111623/100WT/',
#                                fnpre = '100WT_w2m0_111623', wtorhet = 'WT')
# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16mut44_092623', wt_fac =2, mut_fac = 0, 
#                                amp = 1, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111623/100WT/',
#                                fnpre = '100WT_w2m0_111623', wtorhet = 'WT')

# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16mut44_092623', wt_fac =0.2, mut_fac = 0.2, 
#                                amp = 1, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111623/20WT',
#                                fnpre = '20WT_.2.2', wtorhet = 'WT')


# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16mut44_092623', wt_fac =0.4, mut_fac = 0, 
#                                amp = 1, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111623/20WT/',
#                                fnpre = '20WT_wt.4', wtorhet = 'WT')

# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16mut44_092623', wt_fac =1, mut_fac = 2, 
#                                amp = 1, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111623/wt1mut2tTEST1/',
#                                fnpre = '100WT_wt1mut2', wtorhet = 'WT')


# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =1, mut_fac = 1, 
#                                amp = 0.5, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111623/5050HET/',
#                                fnpre = 'HET_111523', wtorhet = 'HET')

# make_currentscape_plot_overexp(na16name = 'na16mut44_092623',na16mut='na16MORAN_100223', wt_fac =1, mut_fac = 1, 
#                                amp = 1, sweep_len = 800, plots_folder = './Plots/12HH16HMM_TF/111623/5050HET/',
#                                fnpre = 'HET_111523', wtorhet = 'HET')


# #na16MORAN_100223
#_________________________________________________________________________________
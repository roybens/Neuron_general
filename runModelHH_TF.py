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
from Na12ModelHH_TF import *
import Na12ModelHH_TF as tf


sim = tf.Na12ModelHH_TF()
#sim = Mature.Na12Model_TF(na12name = 'na12_orig1' , mut_name = 'na12_R850P_tauless2000')
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
print(I.keys())
sim.make_current_scape()
sim.plot_stim()
sim.plot_currents()
sim.plot_volts_dvdt()
sim.plot_fi_curve(0,5,20,fn = f'HH_M1TT_TF')
sim.get_axonal_ks()
sim.plot_axonal_ks()

scan12_16()
#scanK()
dvdt_all_plot()
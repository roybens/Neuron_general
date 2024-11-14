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
import Document as doc
import Tim_ng_functions as nf

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


#   Modifies values in a dictionary stored in a text file.
def modify_dict_file(filename, changes):
#   Args:filename: The name of the text file containing the dictionary.
#       changes: A dictionary containing key-value pairs where the key is the key to modify in the original dictionary and the value is the new value.

  try:
    # Open the file and read its content
    with open(filename, "r") as file:
      content = file.read()

    # Try to load the content as a dictionary
    try:
      data = eval(content)  # Assuming the file contains valid dictionary syntax
    except (NameError, SyntaxError):
      raise ValueError("Invalid dictionary format in the file.")

    # Modify values based on the provided changes dictionary
    for key, value in changes.items():
      if key not in data:
        print(f"Warning: Key '{key}' not found in the dictionary, skipping.")
      else:
        data[key] = value

    # Write the modified dictionary back to the file
    # with open(filename, "w") as file:
    #   file.write(repr(data))
    with open(filename, "w") as file:
      file.write(json.dumps(data, indent=2))  # Add indentation for readability (optional)

  except IOError as e:
    raise ValueError(f"Error opening or writing file: {e}")



# root_path_out = '/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/ManuscriptFigs/Restart030824/6-HMM_focusonTTP_042624/10-12HMMmuts_fitto_1012TTP8_050824'
root_path_out = './Plots/12HMM16HMM/31_vshiftmuts110824_12and16'
# if not os.path.exists(root_path_out):
        # os.makedirs(root_path_out)
        # os.mkdir(root_path_out)



##Adding below function to loop through different na16.mod params        
filename12 = './params/na12_HMM_TEMP_PARAMS.txt'
filename16 = './params/na16_HMM_TEMP_PARAMS.txt'

## Best 12 and 16 params as of 072224
changesna12_071824best ={"a1_0": 3.1547345527269233, "a1_1": 0.05510300665105835, "b1_0": 4.791955661615136, "b1_1": 0.09014477225513692, "a2_0": 3015.155056494468, "a2_1": 0.30987923885393026, "b2_0": 919.3139955076967, "b2_1": 0.41962767235919507, "a3_0": 109.85728965102251, "a3_1": 0.24852254942384186, "b3_0": 1712.2193773613558, "b3_1": 0.01912898529951851, "bh_0": 8.027353908819931, "bh_1": 8.174548719738821, "bh_2": 0.11446203713204262, "ah_0": 0.06601487564289754, "ah_1": 405124.7535686269, "ah_2": 0.08651802346109899, "vShift": -23.438854488000004, "vShift_inact": 15.461948540212093, "maxrate": 11.685304243202804}
changesna16_071624best={"a1_0": 86.82768844997113, "a1_1": 0.12481160483736764, "b1_0": 0.03636308557245105, "b1_1": 0.07299197117480938, "a2_0": 5870.594264277059, "a2_1": 0.20381201621527256, "b2_0": 445.51379959201944, "b2_1": 0.014057437484476853, "a3_0": 1549.7689816436775, "a3_1": 0.08223497094200147, "b3_0": 460.3178077224841, "b3_1": 0.010814365773659428, "bh_0": 13.70152920233826, "bh_1": 9.233117481911744, "bh_2": 0.05775463093748526, "ah_0": 0.7125397402558968, "ah_1": 52695.59895637044, "ah_2": 0.07354314395481377, "vShift": -9.512610605026387, "vShift_inact": 17.512316086445306, "maxrate": 13.917366173297317}

modify_dict_file(filename12, changesna12_071824best)
modify_dict_file(filename16, changesna16_071624best)


simwt = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
                plots_folder = f'{root_path_out}/', pfx=f'WT_', update=True, fac=None) #2-12-{i12}_16-{i16}
wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)

# fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
# simwt.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
# plot_dvdt_from_volts(simwt.volt_soma, simwt.dt, axs[1],clr='cadetblue')
# fig_volts.savefig(f'{simwt.plot_folder}/WT.pdf')


## vshifted hmm fits to move 17 to the right (couldn't tune 082924)
vshift = {"mut24_n2_shift17":{"a1_0": 8.562429512698756, "a1_1": 0.37116193362206645, "b1_0": 5.118968106097008, "b1_1": 0.03813045904092625, "a2_0": 7191.362125327646, "a2_1": 0.050896883767922264, "b2_0": 517.5780649486402, "b2_1": 3.7175711934685567, "a3_0": 421.3306370784977, "a3_1": 0.20205346306383729, "b3_0": 3393.4230352752284, "b3_1": 0.0028520701033402903, "bh_0": 4.6362845301833575, "bh_1": 8.318173978878507, "bh_2": 0.14122000094962656, "ah_0": 8.306931996990492, "ah_1": 9946.74479130471, "ah_2": 0.005184482300621393, "vShift": -16.329406081623784, "vShift_inact": 7.521175378869729, "maxrate": 3561.1403643569074},
"mut234_n2_shift17":{"a1_0": 0.2746528961670398, "a1_1": 0.11059129191212413, "b1_0": 4.693845731194864, "b1_1": 0.015069556625243632, "a2_0": 5295.378778824527, "a2_1": 0.011811932661661206, "b2_0": 909.0436495356778, "b2_1": 1.4435353328294895, "a3_0": 87.67679037560048, "a3_1": 0.0007313444431305495, "b3_0": 1906.5161238747808, "b3_1": 4.9228617014402364e-05, "bh_0": 1.3389085362433701, "bh_1": 0.9213541030945722, "bh_2": 0.18452660613945437, "ah_0": 8.3356323939086, "ah_1": 38756.79360800744, "ah_2": 0.010166242065629497, "vShift": -24.86040292508928, "vShift_inact": 13.204871220678566, "maxrate": 272.08530563122605},
"mut24_n2_shift12":{"a1_0": 1.1519695658044222, "a1_1": 0.043053758953695974, "b1_0": 7.037668427440557, "b1_1": 0.1454018135570699, "a2_0": 33.69082984847775, "a2_1": 0.08222714019795913, "b2_0": 374.81384169243086, "b2_1": 0.05581024660815026, "a3_0": 156.8817451353679, "a3_1": 0.030406259470762628, "b3_0": 1880.189466173783, "b3_1": 0.004244181370281298, "bh_0": 3.6805424920879366, "bh_1": 10.094156020621746, "bh_2": 0.15014712388876933, "ah_0": 7.784801581537402, "ah_1": 678540.0322671022, "ah_2": 0.05062922010233817, "vShift": -30.93971089284024, "vShift_inact": 14.616305834937203, "maxrate": 970.139873914267},
"mut234_n2_shift12":{"a1_0": 2.2486497152981872, "a1_1": 0.0011989013896731154, "b1_0": 1.717779504740911, "b1_1": 0.20327173843369062, "a2_0": 15256.638337027536, "a2_1": 0.03055114159809312, "b2_0": 296.289868494879, "b2_1": 0.05798053651797086, "a3_0": 183.20946668575837, "a3_1": 0.016597181899718476, "b3_0": 4282.0815087924075, "b3_1": 0.10351379466446067, "bh_0": 7.0635956444027155, "bh_1": 15.31283016616241, "bh_2": 0.13193945460304554, "ah_0": 6.487937959475208, "ah_1": 399043.84255955525, "ah_2": 0.04953809946146172, "vShift": -20.854120971888918, "vShift_inact": 10.836523655259075, "maxrate": 4354.4634897591095},
"mut2345_n2_shift12":{"a1_0": 135.32483480425932, "a1_1": 0.7646976594308066, "b1_0": 4.238021102432291, "b1_1": 0.06023608273590855, "a2_0": 2962.033628819678, "a2_1": 0.16628250823695895, "b2_0": 394.7737613225731, "b2_1": 4.074319240094365, "a3_0": 243.1452381570141, "a3_1": 0.009352803012979336, "b3_0": 3060.4856486309163, "b3_1": 0.05410922820397767, "bh_0": 1.8637724005815546, "bh_1": 6.407600833896861, "bh_2": 0.15436684255073352, "ah_0": 1.0449733796067404, "ah_1": 341433.15157095436, "ah_2": 0.09768387679414876, "vShift": -23.592306423324217, "vShift_inact": 3.875606023297248, "maxrate": 2043.568754360027},
"mut24_n2_shift14":{"a1_0": 131.04227948614064, "a1_1": 0.9044012320188759, "b1_0": 3.8794591716832407, "b1_1": 0.027997752010224385, "a2_0": 12217.25416121776, "a2_1": 0.01691598920993581, "b2_0": 463.8214043479611, "b2_1": 2.317907360129902, "a3_0": 377.9765168324716, "a3_1": 0.0011536943084589808, "b3_0": 4812.991178352313, "b3_1": 0.046808957519026646, "bh_0": 6.066050279067019, "bh_1": 16.015320994198312, "bh_2": 0.13770457243013745, "ah_0": 6.050778063754082, "ah_1": 748687.1211853521, "ah_2": 0.05230078867334295, "vShift": -17.53203083276451, "vShift_inact": 6.3709073073068865, "maxrate": 6905.046351691273},
"mut234_n2_shift14":{"a1_0": 0.6302134780595465, "a1_1": 0.13218204822670576, "b1_0": 0.8620712528425807, "b1_1": 0.003619065319614062, "a2_0": 7706.668500785153, "a2_1": 0.1426926682149987, "b2_0": 999.5614483561576, "b2_1": 0.27290410004688437, "a3_0": 264.0980057984137, "a3_1": 0.02185292551071158, "b3_0": 3672.490661427432, "b3_1": 3.592613507223132e-05, "bh_0": 2.979034400827361, "bh_1": 6.3486861291227035, "bh_2": 0.0675485706985279, "ah_0": 23.238018250768675, "ah_1": 42867.85980811481, "ah_2": 0.12396475564751974, "vShift": -26.324142690338867, "vShift_inact": 6.961114503394395, "maxrate": 2599.7088823414583},
"mut2345_n2_shift14":{"a1_0": 65.8000541203561, "a1_1": 0.2113532123734605, "b1_0": 0.47741221264146394, "b1_1": 0.08527308040316821, "a2_0": 3350.1105751689042, "a2_1": 0.13358734406796288, "b2_0": 453.30399122956544, "b2_1": 0.24900961352543272, "a3_0": 243.05190361877496, "a3_1": 0.0010866598243050576, "b3_0": 3400.8554010520106, "b3_1": 0.017575142062584197, "bh_0": 3.9945808289080182, "bh_1": 2.387422826310739, "bh_2": 0.14963730882698245, "ah_0": 3.5504138400955116, "ah_1": 129140.45521258662, "ah_2": 0.024733335222263206, "vShift": -8.051564207202096, "vShift_inact": 4.027202542448445, "maxrate": 698.9201742817049},
"mut24_n2_shift10":{"a1_0": 4.054597578712513, "a1_1": 0.003609774928940823, "b1_0": 7.18158672646337, "b1_1": 0.08520291742319541, "a2_0": 10125.175070597663, "a2_1": 0.15086617983825296, "b2_0": 492.82974085276936, "b2_1": 0.635127856664311, "a3_0": 279.4610790680213, "a3_1": 0.005092564477128638, "b3_0": 4997.70169433507, "b3_1": 0.05295079795380878, "bh_0": 1.9657851998862528, "bh_1": 1.5203421165332864, "bh_2": 0.1485685901352777, "ah_0": 9.093272168976558, "ah_1": 458013.13795717154, "ah_2": 0.08674785230168416, "vShift": -15.262804586271475, "vShift_inact": 3.224969261165757, "maxrate": 1097.0709279850885},
"mut234_n2_shift10":{"a1_0": 5.178092573579475, "a1_1": 4.181691608327789e-05, "b1_0": 0.2131366368552925, "b1_1": 0.12330643712985528, "a2_0": 4653.667086377499, "a2_1": 0.27998119673850436, "b2_0": 436.6257932011715, "b2_1": 2.27270155914251, "a3_0": 106.20105820200216, "a3_1": 0.08203155079360248, "b3_0": 4697.803639460098, "b3_1": 0.037494762358866666, "bh_0": 4.165742068327688, "bh_1": 23.537594271563027, "bh_2": 0.10013635155069628, "ah_0": 0.174213409490662, "ah_1": 165.28496722717045, "ah_2": 0.06057778184282163, "vShift": -36.061776995648515, "vShift_inact": 10.383398735276339, "maxrate": 4399.905055373511},
"mut2345_n2_shift10":{"a1_0": 142.96159717246545, "a1_1": 0.7583784840922501, "b1_0": 2.6641608445655627, "b1_1": 0.08961427897438805, "a2_0": 4607.614812230426, "a2_1": 0.19297636214842573, "b2_0": 117.44029347805376, "b2_1": 0.20343151500215284, "a3_0": 223.87109515364452, "a3_1": 0.00949503471245743, "b3_0": 3550.0972563464984, "b3_1": 0.055260496165779716, "bh_0": 1.7935347017575336, "bh_1": 8.133786258783642, "bh_2": 0.13089508160945554, "ah_0": 0.4209651240890056, "ah_1": 9257.807289069606, "ah_2": 0.02419987398418926, "vShift": -23.559377014001054, "vShift_inact": 6.963061272798676, "maxrate": 1703.1452412705921}}

goodshift = {#"mut234_n2_shift10":{"a1_0": 5.178092573579475, "a1_1": 4.181691608327789e-05, "b1_0": 0.2131366368552925, "b1_1": 0.12330643712985528, "a2_0": 4653.667086377499, "a2_1": 0.27998119673850436, "b2_0": 436.6257932011715, "b2_1": 2.27270155914251, "a3_0": 106.20105820200216, "a3_1": 0.08203155079360248, "b3_0": 4697.803639460098, "b3_1": 0.037494762358866666, "bh_0": 4.165742068327688, "bh_1": 23.537594271563027, "bh_2": 0.10013635155069628, "ah_0": 0.174213409490662, "ah_1": 165.28496722717045, "ah_2": 0.06057778184282163, "vShift": -36.061776995648515, "vShift_inact": 10.383398735276339, "maxrate": 4399.905055373511},
             "mut234_n2_shift12":{"a1_0": 2.2486497152981872, "a1_1": 0.0011989013896731154, "b1_0": 1.717779504740911, "b1_1": 0.20327173843369062, "a2_0": 15256.638337027536, "a2_1": 0.03055114159809312, "b2_0": 296.289868494879, "b2_1": 0.05798053651797086, "a3_0": 183.20946668575837, "a3_1": 0.016597181899718476, "b3_0": 4282.0815087924075, "b3_1": 0.10351379466446067, "bh_0": 7.0635956444027155, "bh_1": 15.31283016616241, "bh_2": 0.13193945460304554, "ah_0": 6.487937959475208, "ah_1": 399043.84255955525, "ah_2": 0.04953809946146172, "vShift": -20.854120971888918, "vShift_inact": 10.836523655259075, "maxrate": 4354.4634897591095}
             }
mut234_n2_shift12={"a1_0": 2.2486497152981872, "a1_1": 0.0011989013896731154, "b1_0": 1.717779504740911, "b1_1": 0.20327173843369062, "a2_0": 15256.638337027536, "a2_1": 0.03055114159809312, "b2_0": 296.289868494879, "b2_1": 0.05798053651797086, "a3_0": 183.20946668575837, "a3_1": 0.016597181899718476, "b3_0": 4282.0815087924075, "b3_1": 0.10351379466446067, "bh_0": 7.0635956444027155, "bh_1": 15.31283016616241, "bh_2": 0.13193945460304554, "ah_0": 6.487937959475208, "ah_1": 399043.84255955525, "ah_2": 0.04953809946146172, "vShift": -20.854120971888918, "vShift_inact": 10.836523655259075, "maxrate": 4354.4634897591095}


n2_110524={
"mut234_n2_shift8.69-4.5":{"a1_0": 190.39777652287304, "a1_1": 0.028536931579245285, "b1_0": 0.8904359828861996, "b1_1": 0.20980652245007603, "a2_0": 1766.740841802121, "a2_1": 0.3801816174681599, "b2_0": 746.0669901976062, "b2_1": 2.449326833382205, "a3_0": 228.66296431222392, "a3_1": 0.05789966713534688, "b3_0": 4589.9859426446355, "b3_1": 0.0021643283886853696, "bh_0": 2.4542026342131273, "bh_1": 10.843017071182047, "bh_2": 0.1218366189269081, "ah_0": 1.0144340132620275, "ah_1": 601521.9632021701, "ah_2": 0.07415598485498767, "vShift": -26.32061617185419, "vShift_inact": 6.327149384219416, "maxrate": 1614.978309838264},
"mut2345_n2_shift8.69-4.5":{"a1_0": 76.84321520220547, "a1_1": 0.32019508183676737, "b1_0": 1.6351554703236393, "b1_1": 0.06733654378153918, "a2_0": 9222.827856236947, "a2_1": 0.008526500523592107, "b2_0": 0.8036638661095896, "b2_1": 1.9109549857562715, "a3_0": 382.25922884589386, "a3_1": 0.04601200960155108, "b3_0": 3529.6576838852843, "b3_1": 0.0009783170802913996, "bh_0": 1.5085496160644865, "bh_1": 0.35001759828803136, "bh_2": 0.15485715015349846, "ah_0": 0.923218627631913, "ah_1": 434347.0647624079, "ah_2": 0.0696568051382046, "vShift": -22.262982835958134, "vShift_inact": 13.641844957238266, "maxrate": 2564.023111804405},
"mut234_n6_shift18-13.5":{"a1_0": 76.84321520220547, "a1_1": 0.32019508183676737, "b1_0": 1.6351554703236393, "b1_1": 0.06733654378153918, "a2_0": 9222.827856236947, "a2_1": 0.008526500523592107, "b2_0": 0.8036638661095896, "b2_1": 1.9109549857562715, "a3_0": 382.25922884589386, "a3_1": 0.04601200960155108, "b3_0": 3529.6576838852843, "b3_1": 0.0009783170802913996, "bh_0": 1.5085496160644865, "bh_1": 0.35001759828803136, "bh_2": 0.15485715015349846, "ah_0": 0.923218627631913, "ah_1": 434347.0647624079, "ah_2": 0.0696568051382046, "vShift": -22.262982835958134, "vShift_inact": 13.641844957238266, "maxrate": 2564.023111804405},}

n2_110824={
# "mut2345_n6_1":{"a1_0": 68.50729357664929, "a1_1": 0.04313512603044619, "b1_0": 0.10836318325268314, "b1_1": 0.0973369915466611, "a2_0": 1773.7990047734415, "a2_1": 0.24930496395330215, "b2_0": 347.0232402200883, "b2_1": 11.946001995512397, "a3_0": 2552.9640262310136, "a3_1": 0.011411814341840798, "b3_0": 472.9688589828079, "b3_1": 0.08286296503749638, "bh_0": 18.290301247882315, "bh_1": 5.112128261704225, "bh_2": 0.08275091786988079, "ah_0": 8.96509600414486, "ah_1": 56394.52673649861, "ah_2": 0.04958708710099484, "vShift": -3.069940806053186, "vShift_inact": 11.773846490059082, "maxrate": 33.53420559541411},
"mut2345_n2_1":{"a1_0": 218.77841406210374, "a1_1": 0.09892803919019888, "b1_0": 3.8883333375643154, "b1_1": 0.24461175809669272, "a2_0": 8064.842219276102, "a2_1": 0.252021445509551, "b2_0": 199.44729115289175, "b2_1": 0.930193462436292, "a3_0": 199.1064435045978, "a3_1": 0.05395219718730044, "b3_0": 2845.3087107406614, "b3_1": 0.0010189863399465509, "bh_0": 4.281730896437004, "bh_1": 9.403756186988014, "bh_2": 0.1238559284157155, "ah_0": 2.794988694030824, "ah_1": 336735.0126425135, "ah_2": 0.060912468962486054, "vShift": -27.733790197814052, "vShift_inact": 12.76189052182388, "maxrate": 3552.61540789386},
"mut2345_n2_2":{"a1_0": 435.2741411895196, "a1_1": 0.20787426237963455, "b1_0": 1.6969946684231483, "b1_1": 0.23654799282457756, "a2_0": 4183.28979419075, "a2_1": 0.023426511496564023, "b2_0": 995.7105577753929, "b2_1": 2.177578553203465, "a3_0": 9.124840564912834, "a3_1": 0.013130776937678217, "b3_0": 1995.2248748646844, "b3_1": 0.08314399529893501, "bh_0": 5.937499205114155, "bh_1": 1.7363736447557045, "bh_2": 0.10462938661338345, "ah_0": 8.545096510704258, "ah_1": 438498.5309352085, "ah_2": 0.060161328217574486, "vShift": -8.880795802150022, "vShift_inact": 19.654942372153045, "maxrate": 14.937363916565737},
"mut2345_n2_3":{"a1_0": 9.290276200004918, "a1_1": 0.007620923784480645, "b1_0": 1.8754449807298448, "b1_1": 0.09601340353830118, "a2_0": 2988.6889448877378, "a2_1": 0.10003846485310891, "b2_0": 488.71956467434813, "b2_1": 0.061194176249668164, "a3_0": 230.44960951993812, "a3_1": 0.07905038828690938, "b3_0": 6387.551754922848, "b3_1": 0.026631463446482793, "bh_0": 5.779582170223426, "bh_1": 9.558419148247305, "bh_2": 0.12081938604157672, "ah_0": 1.0817764327490194, "ah_1": 312093.96363082924, "ah_2": 0.06339100606593855, "vShift": -18.383375902883145, "vShift_inact": 9.22370424168307, "maxrate": 652.3828040980511},
"mut2345_n2_4":{"a1_0": 2.0481531982157124, "a1_1": 0.08941110397772926, "b1_0": 4.17247890069264, "b1_1": 0.12225131702310596, "a2_0": 7644.177368834681, "a2_1": 0.13339608664258643, "b2_0": 407.2376459516906, "b2_1": 0.2753790012247881, "a3_0": 554.6650706480748, "a3_1": 0.014155150125500084, "b3_0": 2656.294956800875, "b3_1": 0.061635360262262434, "bh_0": 6.188946668385947, "bh_1": 3.8076725546649053, "bh_2": 0.10547484746916479, "ah_0": 16.561566890897083, "ah_1": 52464.18467755824, "ah_2": 0.027713797334324386, "vShift": -25.607200132870826, "vShift_inact": 28.514528419369494, "maxrate": 5794.846424222478},}




# n6_101524={"a1_0": 97.66671749868888, "a1_1": 0.03716586306534961, "b1_0": 3.8830728846225977, "b1_1": 0.015017447028888301, "a2_0": 13563.875329376127, "a2_1": 0.17054836408869722, "b2_0": 434.9687960029061, "b2_1": 18.652906007565097, "a3_0": 3718.812738626789, "a3_1": 0.18586319949961275, "b3_0": 328.19038134245005, "b3_1": 0.04394997325690096, "bh_0": 9.019492323918119, "bh_1": 11.087681632354151, "bh_2": 0.058549909026245336, "ah_0": 13.241859443543337, "ah_1": 275895.3332511041, "ah_2": 0.06130990280571661, "vShift": 1.6535349618166855, "vShift_inact": 12.629736455707828, "maxrate": 16.609264160331243}
# modify_dict_file(filename16, n6_101524)

for mutname,dict in n2_110824.items():
  print(f"mutname is {mutname}")
  print(f"it's corresponding dictionary is {dict}")
  modify_dict_file(filename12,dict)
  n6_101524={"a1_0": 97.66671749868888, "a1_1": 0.03716586306534961, "b1_0": 3.8830728846225977, "b1_1": 0.015017447028888301, "a2_0": 13563.875329376127, "a2_1": 0.17054836408869722, "b2_0": 434.9687960029061, "b2_1": 18.652906007565097, "a3_0": 3718.812738626789, "a3_1": 0.18586319949961275, "b3_0": 328.19038134245005, "b3_1": 0.04394997325690096, "bh_0": 9.019492323918119, "bh_1": 11.087681632354151, "bh_2": 0.058549909026245336, "ah_0": 13.241859443543337, "ah_1": 275895.3332511041, "ah_2": 0.06130990280571661, "vShift": 1.6535349618166855, "vShift_inact": 12.629736455707828, "maxrate": 16.609264160331243}
  modify_dict_file(filename16, n6_101524)

  root_path_out = f'./Plots/12HMM16HMM/31_newFits_110824/{mutname}'
  if not os.path.exists(root_path_out):
    os.makedirs(root_path_out)

  
  ###Add variable for new vshifted 16 mut (which ever look good) then make loop for 12 and loop for 16 to iterate through the combos ##091224
  # mutname='mut234_n2_shift12'
  # mut234_n2_shift12={"a1_0": 2.2486497152981872, "a1_1": 0.0011989013896731154, "b1_0": 1.717779504740911, "b1_1": 0.20327173843369062, "a2_0": 15256.638337027536, "a2_1": 0.03055114159809312, "b2_0": 296.289868494879, "b2_1": 0.05798053651797086, "a3_0": 183.20946668575837, "a3_1": 0.016597181899718476, "b3_0": 4282.0815087924075, "b3_1": 0.10351379466446067, "bh_0": 7.0635956444027155, "bh_1": 15.31283016616241, "bh_2": 0.13193945460304554, "ah_0": 6.487937959475208, "ah_1": 399043.84255955525, "ah_2": 0.04953809946146172, "vShift": -20.854120971888918, "vShift_inact": 10.836523655259075, "maxrate": 4354.4634897591095}
  # mut24_n6_shift10={"a1_0": 94.75905990157207, "a1_1": 0.018023703763738824, "b1_0": 0.31023493687676373, "b1_1": 0.09008967082413695, "a2_0": 5907.736073687958, "a2_1": 0.23518065657745135, "b2_0": 419.89073598002807, "b2_1": 1.4619587126350462, "a3_0": 1196.957340421589, "a3_1": 0.04846855255279074, "b3_0": 499.9066090356164, "b3_1": 0.0021881262762982706, "bh_0": 20.254408529692903, "bh_1": 6.342454458189579, "bh_2": 0.06112691568909393, "ah_0": 14.217056459991783, "ah_1": 192666.54983024174, "ah_2": 0.06340953132391121, "vShift": -1.844506962628052, "vShift_inact": 16.738301924225823, "maxrate": 11.46203465759279}
  
## New fits for 1.2 and 1.6 following Kevin's guidance on HH model.
# n6_102524={"a1_0": 97.66671749868888, "a1_1": 0.03716586306534961, "b1_0": 3.8830728846225977, "b1_1": 0.015017447028888301, "a2_0": 13563.875329376127, "a2_1": 0.17054836408869722, "b2_0": 434.9687960029061, "b2_1": 18.652906007565097, "a3_0": 3718.812738626789, "a3_1": 0.18586319949961275, "b3_0": 328.19038134245005, "b3_1": 0.04394997325690096, "bh_0": 9.019492323918119, "bh_1": 11.087681632354151, "bh_2": 0.058549909026245336, "ah_0": 13.241859443543337, "ah_1": 275895.3332511041, "ah_2": 0.06130990280571661, "vShift": 1.6535349618166855, "vShift_inact": 12.629736455707828, "maxrate": 16.609264160331243}
# n2_102524={"a1_0": 77.5290880057393, "a1_1": 0.8534705914137256, "b1_0": 1.2034064865578407, "b1_1": 0.014785144308705655, "a2_0": 6205.9038993807335, "a2_1": 0.0392413842323337, "b2_0": 846.6014010105109, "b2_1": 1.9624857335743886, "a3_0": 105.50670247235922, "a3_1": 0.050163170583720884, "b3_0": 1912.6907848541457, "b3_1": 0.0002336951139489255, "bh_0": 5.486172056286093, "bh_1": 8.025517130836056, "bh_2": 0.10509571449338692, "ah_0": 14.036037851882138, "ah_1": 2718.2515522564354, "ah_2": 0.0035793633476156363, "vShift": -26.804997176209856, "vShift_inact": 8.28564108853396, "maxrate": 1690.0489804575473}

# modify_dict_file(filename12, n2_110524)
# modify_dict_file(filename16,n6_102524)

  
        

  simtim = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
                ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
                plots_folder = f'{root_path_out}/', pfx=f'WT_', update=True, fac=None) #2-12-{i12}_16-{i16}
  simtim.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'{mutname}-WTvshiftmut')#vs_amp=[0.5]

# ##Plotting only WT Stim/DVDT and Currentscapes
# fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
# simwt.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
# plot_dvdt_from_volts(simwt.volt_soma, simwt.dt, axs[1],clr='cadetblue')
# fig_volts.savefig(f'{simwt.plot_folder}/WT.pdf')

##Get states of HMM (plot_8states in NeuronModelClass.py)
# fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
# ap_t, vm_t = simwt.plot_stim(axs=axs[0],stim_amp = 0.5,dt=0.005, clr='cadetblue') #dt=0.005
# nf.plot_8states(csv_name="./Plots/Channel_state_plots/na12_channel_states.csv", outfile_sfx="na12_072924",start = 27500,stop=30000,ap_t=ap_t, vm_t=vm_t )
# nf.plot_8states(csv_name="./Plots/Channel_state_plots/na16_channel_states.csv", outfile_sfx="na16_072924",start = 27500,stop=30000,ap_t=ap_t, vm_t=vm_t )

# simwt.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200)  
# simwt.plot_model_FI_Vs_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WT_',wt_fi = [0, 0, 3, 7, 9, 10, 10, 11, 12, 12, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 18])#fnpre=f'{mutTXT}')

# simwt.make_currentscape_plot(amp=0.5, time1=100,time2=400,stim_start=100, sweep_len=800)
# simwt.make_currentscape_plot(amp=0.5, time1=50,time2=200,stim_start=30, sweep_len=200)  



# fac=1
  for fac in (0.1,10,100):
# # for fac in (2,4,10,50,100,1000):
# # for factor in [2,2.5,3,3.5,4]:

# sim_wt = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
#                                     ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
#                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
#                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
#                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
#                                     pfx=f'{str(fac)}', update=True, fac=None)
# # wt_Vm1,_,wt_t1,_ = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = config) #stim_amp=0.5
# sim_wt.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac-{str(fac)}')
# wt_fi=simwt.plot_fi_curve_2line(wt_data=None,wt2_data=None,start=-0.4,end=1,nruns=140, fn=f'WT')
# simwt.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200,pfx='WT')

# simhet = tf.Na12Model_TF(ais_nav12_fac=(2*100)/2,ais_nav16_fac=10*4,nav12=(3*3)/2,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
#                                     ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
#                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
#                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
#                                     params_folder='./params/', plots_folder=f'{root_path_out}/24-longsweep_wthetko', 
#                                     pfx=f'{str(fac)}', update=True)
# het_Vm1,_,het_t1,_ = simhet.get_stim_raw_data(stim_amp =0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma) #sim_config for changing regions
# simhet.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'het-{str(fac)}')
# het_fi=simhet.plot_fi_curve_2line(wt_data=wt_fi,wt2_data=None,start=-0.4,end=1,nruns=140, fn=f'WTHET')
# simhet.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200,pfx='HET')

# simko = tf.Na12Model_TF(ais_nav12_fac=(2*100)*0,ais_nav16_fac=10*4,nav12=(3*3)*0,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10, #nav12=3*2*1.5
#                                     ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
#                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
#                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
#                                     params_folder='./params/', plots_folder=f'{root_path_out}/24-longsweep_wthetko', 
#                                     pfx=f'{str(fac)}', update=True)
# simko.plot_fi_curve_2line(wt_data=wt_fi,wt2_data=het_fi,start=-0.4,end=1,nruns=140, fn=f'WTHETKO')
# simko.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,het_Vm=het_Vm1,het_t=het_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'WTvHETvKO')#vs_amp=[0.5]
# simko.make_currentscape_plot(amp=0.5, time1=50,time2=100,stim_start=30, sweep_len=200,pfx='KO')




    # somaK Iteration
    sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5, somaK=50*0.25*fac, KP=1000*3.56, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_somaK{str(fac)}', update=True)
    sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac-{str(fac)}')

    # KT Iteration
    sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10*fac,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KT{str(fac)}', update=True)
    sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac-{str(fac)}')
    
    # ais_ca Iteration
    sim_test_ais_ca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*4*4,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                  ais_ca = 100*fac,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_ais_Kca{str(fac)}', update=True)
    sim_test_ais_ca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_ca_fac-{str(fac)}')
    
    # ais_Kca Iteration
    sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*4*4,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_ais_Kca{str(fac)}', update=True)
    sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac-{str(fac)}')


    sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56*fac, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KP{str(fac)}', update=True)
    sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac-{str(fac)}')

    # ais_nav12_fac Iteration
    sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*100*fac,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_ais_nav12_fac{str(fac)}', update=True)
    sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac-{str(fac)}')

    # ais_nav16_fac Iteration
    sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4*fac,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_ais_nav16_fac{str(fac)}', update=True)
    sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac-{str(fac)}')

    # nav12 Iteration
    sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3*fac,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_nav12{str(fac)}', update=True)
    sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac-{str(fac)}')

    # nav16 Iteration
    sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5*fac, somaK=50*0.25, KP=1000*3.56, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_nav16{str(fac)}', update=True)
    sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac-{str(fac)}')

    # soma_na12 Iteration
    sim_test_soma_na12 = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5*fac, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_soma_na12{str(fac)}', update=True)
    sim_test_soma_na12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na12_fac-{str(fac)}')

    # soma_na16 Iteration
    sim_test_soma_na16 = tf.Na12Model_TF(ais_nav12_fac=2*100,ais_nav16_fac=10*4*4,nav12=3*3,nav16=7.5, somaK=50*0.25, KP=1000*3.56, KT=10,
                                  ais_ca = 100,ais_Kca = 5*0.01, soma_na12=2.5, soma_na16=1*fac, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_soma_na16{str(fac)}', update=True)
    sim_test_soma_na16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na16_fac-{str(fac)}')
    






'''
    sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1*fac, KP=1000, KT=10,
                                      ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                      pfx=f'WT_somaK_fac{str(fac)}', update=True)
    sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac{str(fac)}')

    # KT Iteration
    sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10*fac,
                                  ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KT_fac{str(fac)}', update=True)
    sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac{str(fac)}')


    # ais_Kca Iteration
    sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                        na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                        na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                        pfx=f'WT_ais_Kca{str(fac)}', update=True)
    sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac{str(fac)}')

    sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                    na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                    na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_KP{str(fac)}', update=True)
    sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac{str(fac)}')
        



  # soma_na12 Iteration
    sim_test_soma_na12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5*fac, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_soma_na12{str(fac)}', update=True)
    sim_test_soma_na12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na12_fac{str(fac)}')

    # soma_na16 Iteration
    sim_test_soma_na16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1*fac, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_soma_na16{str(fac)}', update=True)
    sim_test_soma_na16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na16_fac{str(fac)}')

    
    sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3*fac,nav16=7.5, somaK=1, KP=1000, KT=10,
                                      ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                      pfx=f'WT_nav12_fac{str(fac)}', update=True)
    sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac{str(fac)}')

    # nav16 Iteration
    sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5*fac, somaK=1, KP=1000, KT=10,
                                      ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                      pfx=f'WT_nav16_fac{str(fac)}', update=True)
    sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac{str(fac)}')

    

    sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*fac,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                              ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                              na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                              na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                              params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav12_fac{str(fac)}', update=True)
    sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac{str(fac)}')

    # ais_nav16_fac Iteration
    sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*fac,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                            ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                            na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                            na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                            params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav16_fac{str(fac)}', update=True)
    sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac{str(fac)}')




  # somaK Iteration
    sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1*fac, KP=1000, KT=10,
                                      ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                      pfx=f'WT_somaK_fac{str(fac)}', update=True)
    sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac{str(fac)}')

    # KT Iteration
    sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10*fac,
                                  ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KT_fac{str(fac)}', update=True)
    sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac{str(fac)}')

    # ais_ca Iteration
    sim_test_ais_ca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                      ais_ca = 100*fac,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                      pfx=f'WT_ais_ca_fac{str(fac)}', update=True)
    sim_test_ais_ca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_ca_fac{str(fac)}')

    # ais_Kca Iteration
    sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                        na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                        na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                        pfx=f'WT_ais_Kca_fac{str(fac)}', update=True)
    sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac{str(fac)}')
  

     
        sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*fac,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                                ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                                params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav12_fac{str(fac)}', update=True)
        sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac{str(fac)}')

        # ais_nav16_fac Iteration
        sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*fac,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                                ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                                params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav16_fac{str(fac)}', update=True)
        sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac{str(fac)}')

        # nav12 Iteration
        sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3*fac,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_nav12{str(fac)}', update=True)
        sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac{str(fac)}')

        # nav16 Iteration
        sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5*fac, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_nav16{str(fac)}', update=True)
        sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac{str(fac)}')

        # KP Iteration
        sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                    na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                    na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_KP{str(fac)}', update=True)
        sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac{str(fac)}')
        

  '''















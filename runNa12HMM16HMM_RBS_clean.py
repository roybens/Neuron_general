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
root_path_out = './Plots/12HMM16HMM/16-RBSiteratev2'

if not os.path.exists(root_path_out):
        os.makedirs(root_path_out)
        # os.mkdir(root_path_out)



##Adding below function to loop through different na16.mod params        
# filename = "/global/homes/t/tfenton/Neuron_general-2/params/na12_HMM_TF100923-2.txt" ##TF031524 for changing 8st na12
filename12 = './params/na12_HMM_TEMP_PARAMS.txt'
filename16 = './params/na16_HMM_TEMP_PARAMS.txt'


                
##TF052024 mut10_12_TTP8 (from 050624) better WT (fit to mut10_9_TTP8)
changesna12={"a1_0": 62.774771313021546, 
        "a1_1": 0.6854152336583206,
        "b1_0": 3.2117067311143277,
        "b1_1": 0.1432460480232296, 
        "a2_0": 2468.966900014909,
        "a2_1": 0.0834387238328, 
        "b2_0": 490.16060600231606,
        "b2_1": 2.969500725999265,
        "a3_0": 190.5883640336242,
        "a3_1": 0.003108395956123883,
        "b3_0": 7689.251014289831, 
        "b3_1": 0.04054164070835632,
        "bh_0": 4.063594186259147,
        "bh_1": 2.115884898210715, 
        "bh_2": 0.1433653421971472,
        "ah_0": 1.3563238605774417,
        "ah_1": 6568.351916792737, 
        "ah_2": 0.011127551783912584,
        "vShift": -18.276678986708095, 
        "vShift_inact": 16.74204011921361, 
        "maxrate": 6.170113221706686}

##mut10_4, testing for altered tau WT 061124                
# changesna12={"a1_0": 30.990568607464937, "a1_1": 0.727207131085451, "b1_0": 2.4177659248112304, "b1_1": 0.001361137402837942, "a2_0": 7764.878961142766, "a2_1": 0.033710133967452593, "b2_0": 354.5075793923026, "b2_1": 4.0585190172293055, "a3_0": 124.65125337416927, "a3_1": 0.002466385979914096, "b3_0": 5691.006145002193, "b3_1": 0.0062791739575876, "bh_0": 0.7148812999656258, "bh_1": 1.0205850850329137, "bh_2": 0.1491648507752708, "ah_0": 11.231511989775173, "ah_1": 29046.460566891234, "ah_2": 0.008490668279800669, "vShift": -19.00612418597558, "vShift_inact": 8.677200690072695, "maxrate": 5.262143195447436}

##TF052824 16HMM WT from Moran na16mut44_092623
changesna16={"a1_0": 9.943980540891205, 
        "a1_1": 0.09023475298110195, 
        "b1_0": 4.809469162333778, 
        "b1_1": 0.00021253413520036122, 
        "a2_0": 3699.864927408996, 
        "a2_1": 0.014825840578195144, 
        "b2_0": 32.94719611096497, 
        "b2_1": 0.043572007893336887,
        "a3_0": 428.4532637061227, 
        "a3_1": 0.1993700855837062, 
        "b3_0": 45.50266263937303, 
        "b3_1": 0.004565244221972131,
        "bh_0": 6.623769188984069, 
        "bh_1": 7.348567323368201, 
        "bh_2": 0.13171436477580875, 
        "ah_0": 5.722632232902148, 
        "ah_1": 1820.0789387156779, 
        "ah_2": 0.013864995417150049, 
        "vShift": -9.719627438867658, 
        "vShift_inact": 3.2360259605403203, 
        "maxrate": 54.784511287581864}

changesna16a={"a1_0": 8.0578874919151, "a1_1": 0.0362460004441742, "b1_0": 0.2975424360004787, "b1_1": 0.019626504231602726, "a2_0": 7541.367908495317, "a2_1": 0.008115928598620786, "b2_0": 37.78264401293287, "b2_1": 13.197541674645006, "a3_0": 2661.4548837273387, "a3_1": 0.28322186815760786, "b3_0": 41.45025415671522, "b3_1": 0.005946538949708524, "bh_0": 4.957064052666118, "bh_1": 14.94315170855162, "bh_2": 0.10627633864486724, "ah_0": 0.3348261287268917, "ah_1": 1847.8521286814391, "ah_2": 0.04174076351521052, "vShift": -9.569584432015834, "vShift_inact": 2.352045239220809, "maxrate": 44.84946684890218}
changesna16b = {"a1_0": 9.090328600911736, "a1_1": 0.011144987169071197, "b1_0": 9.255699008849243, "b1_1": 0.0016137523402601096, "a2_0": 10932.78658636546, "a2_1": 0.29192427179674435, "b2_0": 15.767473317100103, "b2_1": 25.93317454739589, "a3_0": 390.30935790084703, "a3_1": 0.025356749923664747, "b3_0": 46.64622013957142, "b3_1": 0.018170036985660443, "bh_0": 1.6059822779031636, "bh_1": 3.7393826933625283, "bh_2": 0.1426405180186169, "ah_0": 2.2070454502199075, "ah_1": 38282.91375852737, "ah_2": 0.08991604167580454, "vShift": -8.808787096096369, "vShift_inact": -3.981655239131775, "maxrate": 36.56718201895245}

#This is the 12hmm params most updated from 071424
changesna12_071524best = {"mut2345_5_TTP8":{"a1_0": 10.944737670133605, "a1_1": 0.2034183732842103, "b1_0": 4.815478417469935, "b1_1": 0.043356252117941904, "a2_0": 5405.880730210139, "a2_1": 0.18763689314759507, "b2_0": 867.850712446166, "b2_1": 4.253173302744734, "a3_0": 343.3028879363021, "a3_1": 0.02687246485446145, "b3_0": 5124.498264970646, "b3_1": 8.51262772092558e-05, "bh_0": 4.2389048788776575, "bh_1": 7.807124232192017, "bh_2": 0.12001212159063362, "ah_0": 1.2727492058102337, "ah_1": 260406.1761436006, "ah_2": 0.06430725966278353, "vShift": -20.247520697302086, "vShift_inact": 4.401183916926222, "maxrate": 10.438035930256888}}

##Uncomment if want to update params file to update mod file!!!
modify_dict_file(filename12, changesna12_071524best)
modify_dict_file(filename16, changesna16b)





### 12 ###
## HOF params from 1.2hmm runs from 071824
changesna12_071824 ={"2-mut10_10":{"a1_0": 3.1547345527269233, "a1_1": 0.05510300665105835, "b1_0": 4.791955661615136, "b1_1": 0.09014477225513692, "a2_0": 3015.155056494468, "a2_1": 0.30987923885393026, "b2_0": 919.3139955076967, "b2_1": 0.41962767235919507, "a3_0": 109.85728965102251, "a3_1": 0.24852254942384186, "b3_0": 1712.2193773613558, "b3_1": 0.01912898529951851, "bh_0": 8.027353908819931, "bh_1": 8.174548719738821, "bh_2": 0.11446203713204262, "ah_0": 0.06601487564289754, "ah_1": 405124.7535686269, "ah_2": 0.08651802346109899, "vShift": -23.438854488000004, "vShift_inact": 15.461948540212093, "maxrate": 11.685304243202804},
  "2-mut10_11":{"a1_0": 123.55164475504156, "a1_1": 0.18280725795896624, "b1_0": 2.5031412969696896, "b1_1": 0.07026748522211855, "a2_0": 2463.2197792143124, "a2_1": 0.004238861290533136, "b2_0": 38.43843407001073, "b2_1": 0.20850090279571298, "a3_0": 460.1783887546581, "a3_1": 0.00025098008309614047, "b3_0": 2619.517298555078, "b3_1": 0.0026115522418630344, "bh_0": 6.9883906147158825, "bh_1": 2.5595587272547498, "bh_2": 0.11716804680086335, "ah_0": 9.707385862461836, "ah_1": 1090337.4679787222, "ah_2": 0.05859708789903573, "vShift": -15.01880759926982, "vShift_inact": 12.808190670436819, "maxrate": 495.5106917827947},
  "2-mut10_13":{"a1_0": 1.1936241470307003, "a1_1": 0.00041128579093632246, "b1_0": 0.32926727954173063, "b1_1": 0.054261510020281366, "a2_0": 8551.5502281774, "a2_1": 0.10597991960521258, "b2_0": 457.593135922957, "b2_1": 1.4341816064142605, "a3_0": 267.499299729361, "a3_1": 0.008074596433951422, "b3_0": 2254.8151962384695, "b3_1": 0.010510942364516131, "bh_0": 4.805630210944513, "bh_1": 2.9835232417075543, "bh_2": 0.1045009188057163, "ah_0": 4.045500225596787, "ah_1": 368941.7237931994, "ah_2": 0.04529204416022142, "vShift": -21.156914313772255, "vShift_inact": 20.859307205916892, "maxrate": 4961.460117156864},
  "2-mut10_21":{"a1_0": 1.9443819293948996, "a1_1": 0.0015954854218298538, "b1_0": 4.473696742259939, "b1_1": 0.007930753885905788, "a2_0": 9063.9125910059, "a2_1": 0.06171530204555184, "b2_0": 841.111215677911, "b2_1": 0.11325108618516766, "a3_0": 435.8164871677171, "a3_1": 0.1364934781124262, "b3_0": 4720.2915734996495, "b3_1": 0.03849612308236557, "bh_0": 8.749346428916462, "bh_1": 12.099017871822932, "bh_2": 0.10716363374872065, "ah_0": 2.3063140524367527, "ah_1": 88014.79163239506, "ah_2": 0.06539467228615606, "vShift": -31.619387013472252, "vShift_inact": 20.585169487908036, "maxrate": 1526.3240301091982},
  "2-mut10_22":{"a1_0": 180.5025927339404, "a1_1": 0.33113244897361693, "b1_0": 2.0767707269553695, "b1_1": 0.6223355075560818, "a2_0": 13435.407811732272, "a2_1": 0.0211117695738876, "b2_0": 999.6095479500625, "b2_1": 1.2704801705763988, "a3_0": 89.34732446514457, "a3_1": 0.09733165771102899, "b3_0": 4221.576967234849, "b3_1": 0.0027725825221146267, "bh_0": 3.046647653540372, "bh_1": 4.5808799713466355, "bh_2": 0.10576328857383457, "ah_0": 5.737541971269167, "ah_1": 71131.21529249132, "ah_2": 0.04175868116559203, "vShift": -21.307663009347962, "vShift_inact": 12.11121381517722, "maxrate": 8.130169957341023},
  "2-mut10_23":{"a1_0": 369.5821967702335, "a1_1": 0.39038766418717896, "b1_0": 3.6822596946228625, "b1_1": 0.10501327129522635, "a2_0": 6910.772943638965, "a2_1": 0.11524642871770532, "b2_0": 837.8273305352495, "b2_1": 9.992266951279685, "a3_0": 405.5619250571541, "a3_1": 0.10344605522437034, "b3_0": 2195.831730666804, "b3_1": 0.002193364936230799, "bh_0": 3.2077194944857705, "bh_1": 5.8038639138520285, "bh_2": 0.07519588072397472, "ah_0": 0.008950112120804876, "ah_1": 278687.5293292866, "ah_2": 0.4251840107939006, "vShift": -19.752132240171534, "vShift_inact": 6.576656557191882, "maxrate": 8.856994920438126}}

changesna12_071824best ={"2-mut10_10":{"a1_0": 3.1547345527269233, "a1_1": 0.05510300665105835, "b1_0": 4.791955661615136, "b1_1": 0.09014477225513692, "a2_0": 3015.155056494468, "a2_1": 0.30987923885393026, "b2_0": 919.3139955076967, "b2_1": 0.41962767235919507, "a3_0": 109.85728965102251, "a3_1": 0.24852254942384186, "b3_0": 1712.2193773613558, "b3_1": 0.01912898529951851, "bh_0": 8.027353908819931, "bh_1": 8.174548719738821, "bh_2": 0.11446203713204262, "ah_0": 0.06601487564289754, "ah_1": 405124.7535686269, "ah_2": 0.08651802346109899, "vShift": -23.438854488000004, "vShift_inact": 15.461948540212093, "maxrate": 11.685304243202804},
  "2-mut10_22":{"a1_0": 180.5025927339404, "a1_1": 0.33113244897361693, "b1_0": 2.0767707269553695, "b1_1": 0.6223355075560818, "a2_0": 13435.407811732272, "a2_1": 0.0211117695738876, "b2_0": 999.6095479500625, "b2_1": 1.2704801705763988, "a3_0": 89.34732446514457, "a3_1": 0.09733165771102899, "b3_0": 4221.576967234849, "b3_1": 0.0027725825221146267, "bh_0": 3.046647653540372, "bh_1": 4.5808799713466355, "bh_2": 0.10576328857383457, "ah_0": 5.737541971269167, "ah_1": 71131.21529249132, "ah_2": 0.04175868116559203, "vShift": -21.307663009347962, "vShift_inact": 12.11121381517722, "maxrate": 8.130169957341023}}

### 12 ###

##########################


### 16HMM params from 071624 ###
changesna16_071624={
# "mut2345_7_TTP14":{"a1_0": NaN, "a1_1": 0.06938776718829234, "b1_0": 9.299764613294178, "b1_1": 0.03075010806196215, "a2_0": 5510.406149068496, "a2_1": 0.14342331502980615, "b2_0": 455.86584978604185, "b2_1": 2.4055988314625014, "a3_0": 1077.658771213025, "a3_1": 0.02464686704320922, "b3_0": 498.7332821005065, "b3_1": 0.03373053771177986, "bh_0": 36.129058140313944, "bh_1": 3.3950562218997855, "bh_2": 0.0906904466563052, "ah_0": 6.194679529012888, "ah_1": 282630.06048083666, "ah_2": 0.06340446980700913, "vShift": -9.835732851954909, "vShift_inact": 13.767509089998114, "maxrate": 29.20212075051712},
"mut2345_7_TTP12":{"a1_0": 85.6588238133349, "a1_1": 0.0202022079990265, "b1_0": 0.3099570656014148, "b1_1": 0.05881415977134272, "a2_0": 16158.257195963906, "a2_1": 0.005086976728930723, "b2_0": 499.99226772525736, "b2_1": 0.7835296601566557, "a3_0": 569.8952378926141, "a3_1": 0.16118608974939236, "b3_0": 495.21533544011476, "b3_1": 0.0012946186534438207, "bh_0": 4.7651418855856384, "bh_1": 0.32365976689273107, "bh_2": 0.032441160564102435, "ah_0": 8.216321142786994, "ah_1": 108092.90417639431, "ah_2": 0.11409214556524883, "vShift": -9.953363767461909, "vShift_inact": 8.73207432283476, "maxrate": 7.143837339905652},
# "mut2345_7_TTP14":{"a1_0": NaN, "a1_1": 0.06938776718829234, "b1_0": 9.299764613294178, "b1_1": 0.03075010806196215, "a2_0": 5510.406149068496, "a2_1": 0.14342331502980615, "b2_0": 455.86584978604185, "b2_1": 2.4055988314625014, "a3_0": 1077.658771213025, "a3_1": 0.02464686704320922, "b3_0": 498.7332821005065, "b3_1": 0.03373053771177986, "bh_0": 36.129058140313944, "bh_1": 3.3950562218997855, "bh_2": 0.0906904466563052, "ah_0": 6.194679529012888, "ah_1": 282630.06048083666, "ah_2": 0.06340446980700913, "vShift": -9.835732851954909, "vShift_inact": 13.767509089998114, "maxrate": 29.20212075051712},
"mut2345_7_TTP15":{"a1_0": 86.82768844997113, "a1_1": 0.12481160483736764, "b1_0": 0.03636308557245105, "b1_1": 0.07299197117480938, "a2_0": 5870.594264277059, "a2_1": 0.20381201621527256, "b2_0": 445.51379959201944, "b2_1": 0.014057437484476853, "a3_0": 1549.7689816436775, "a3_1": 0.08223497094200147, "b3_0": 460.3178077224841, "b3_1": 0.010814365773659428, "bh_0": 13.70152920233826, "bh_1": 9.233117481911744, "bh_2": 0.05775463093748526, "ah_0": 0.7125397402558968, "ah_1": 52695.59895637044, "ah_2": 0.07354314395481377, "vShift": -9.512610605026387, "vShift_inact": 17.512316086445306, "maxrate": 13.917366173297317},
"mut2345_7_TTP16":{"a1_0": 99.77093685460736, "a1_1": 0.06952447237043777, "b1_0": 44.488937274051395, "b1_1": 0.01437157174013319, "a2_0": 13786.880239302009, "a2_1": 0.04728044123794761, "b2_0": 371.9616790346747, "b2_1": 0.982926960007191, "a3_0": 1100.142746646376, "a3_1": 0.16972738365432105, "b3_0": 398.8689876384367, "b3_1": 1.923218413077037, "bh_0": 27.97787477969485, "bh_1": 7.509181066635014, "bh_2": 0.0654334243601804, "ah_0": 26.88150543572732, "ah_1": 446454.58231950586, "ah_2": 0.058416530449989235, "vShift": -5.942474759747714, "vShift_inact": 13.574433174223056, "maxrate": 5.65879534144022},
# "mut2345_7_TTP17":{"a1_0": 81.96123507176391, "a1_1": 0.06987360281960636, "b1_0": 22.233852097469732, "b1_1": 0.005289482823934211, "a2_0": 9449.409229311088, "a2_1": 0.012682330543673702, "b2_0": 415.43005237394215, "b2_1": 12.02353261410434, "a3_0": 241.23476684702348, "a3_1": 0.155770733130927, "b3_0": NaN, "b3_1": 0.034843907915717565, "bh_0": 4.608497930985928, "bh_1": 3.221848689282568, "bh_2": 0.06356038365364591, "ah_0": 0.07677508177652914, "ah_1": 266768.49231595645, "ah_2": 0.18043015027863882, "vShift": -9.953370986042636, "vShift_inact": -5.955363501341428, "maxrate": 6.047682747947052},
"mut2345_7_TTP18":{"a1_0": 63.52687247769865, "a1_1": 0.05130703643336672, "b1_0": 0.13579074240381706, "b1_1": 0.038528966888720075, "a2_0": 19307.838394509618, "a2_1": 0.22255370049675877, "b2_0": 287.76891739586813, "b2_1": 18.999936742463266, "a3_0": 3134.804039682592, "a3_1": 0.1923862611629993, "b3_0": 495.7538910887652, "b3_1": 0.8729867568853192, "bh_0": 6.704358394495574, "bh_1": 6.777560116136677, "bh_2": 0.06444675240720582, "ah_0": 23.74307966097871, "ah_1": 7811.952615857546, "ah_2": 0.018131346588346812, "vShift": -7.957263237920417, "vShift_inact": -5.876473293292756, "maxrate": 4.575238073306082}}

changesna16_071624best={"mut2345_7_TTP15":{"a1_0": 86.82768844997113, "a1_1": 0.12481160483736764, "b1_0": 0.03636308557245105, "b1_1": 0.07299197117480938, "a2_0": 5870.594264277059, "a2_1": 0.20381201621527256, "b2_0": 445.51379959201944, "b2_1": 0.014057437484476853, "a3_0": 1549.7689816436775, "a3_1": 0.08223497094200147, "b3_0": 460.3178077224841, "b3_1": 0.010814365773659428, "bh_0": 13.70152920233826, "bh_1": 9.233117481911744, "bh_2": 0.05775463093748526, "ah_0": 0.7125397402558968, "ah_1": 52695.59895637044, "ah_2": 0.07354314395481377, "vShift": -9.512610605026387, "vShift_inact": 17.512316086445306, "maxrate": 13.917366173297317}}
### 16 ###




##TF072124 With the current indenting, this will loop through the 6 new synthetic muts 1.2hmm's in changesna12_071824, then continue to compare to the subsequent tested param*fac
for mutname,dict in changesna12_071824.items():
  print(f"mutname is {mutname}")
  print(f"it's corresponding dictionary is {dict}")
  modify_dict_file(filename12,dict)
        # modify_dict_file(filename16,dict)

        
  simwt = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10, ##070324 nav12=3, nav16=4 ##062424 ais_nav12_fac=10,ais_nav16_fac=10,nav12=4,nav16=2.5 #ais_nav12_fac=7,ais_nav16_fac=7,nav12=2.5,nav16=2.5, somaK=1, KP=50, KT=10
              ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,#somaK=90, KP=20, KT=6,#somaK=30,  KP=40, ##This row all 1 default
              na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
              na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],params_folder = './params/',
              plots_folder = f'{root_path_out}/', pfx=f'WT_', update=True) #2-12-{i12}_16-{i16}
  wt_Vm1,wt_I1,wt_t1,wt_stim1 = simwt.get_stim_raw_data(stim_amp = 0.5,dt=0.005,rec_extra=False,stim_dur=500, sim_config = sim_config_soma)
    
    ### AIS12/16 and nav12/16
  for fac in (0.5,2,0.25,4,0.1, 10,0.01,100,5,50):
  #for fac in (2,3,5,1.25,1.5):
  # somaK Iteration
    sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50*fac, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                    na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                    na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                    pfx=f'WT_somaK{str(fac).replace(".", "_")}', update=True)
    sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac{str(fac).replace(".", "_")}')

    # KT Iteration
    sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10*fac,
                                  ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KT{str(fac).replace(".", "_")}', update=True)
    sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac{str(fac).replace(".", "_")}')

    # ais_Kca Iteration
    sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                      ais_ca = 100,ais_Kca = 5*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                      pfx=f'WT_ais_Kca{str(fac).replace(".", "_")}', update=True)
    sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac{str(fac).replace(".", "_")}')

    sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                  ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KP{str(fac).replace(".", "_")}', update=True)
    sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac{str(fac).replace(".", "_")}')

    # ais_nav12_fac Iteration
    sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*fac,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                            ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                            na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                            na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                            params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                            pfx=f'WT_ais_nav12_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac{str(fac).replace(".", "_")}')

    # ais_nav16_fac Iteration
    sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*fac,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                            ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                            na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                            na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                            params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                            pfx=f'WT_ais_nav16_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac{str(fac).replace(".", "_")}')

    # nav12 Iteration
    sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3*fac,nav16=7.5, somaK=50, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                    na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                    na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                    pfx=f'WT_nav12{str(fac).replace(".", "_")}', update=True)
    sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac{str(fac).replace(".", "_")}')

    # nav16 Iteration
    sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5*fac, somaK=50, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                    na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                    na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                    pfx=f'WT_nav16{str(fac).replace(".", "_")}', update=True)
    sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac{str(fac).replace(".", "_")}')

    # soma_na12 Iteration
    sim_test_soma_na12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5*fac, soma_na16=1, dend_nav12=1, node_na=1,
                                        na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                        na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                        pfx=f'WT_soma_na12{str(fac).replace(".", "_")}', update=True)
    sim_test_soma_na12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na12_fac{str(fac).replace(".", "_")}')

    # soma_na16 Iteration
    sim_test_soma_na16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=50, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1*fac, dend_nav12=1, node_na=1,
                                        na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                        na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                        pfx=f'WT_soma_na16{str(fac).replace(".", "_")}', update=True)
    sim_test_soma_na16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na16_fac{str(fac).replace(".", "_")}')


'''
    sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1*fac, KP=1000, KT=10,
                                     ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                     pfx=f'WT_somaK_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac{str(fac).replace(".", "_")}')

    # KT Iteration
    sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10*fac,
                                  ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KT_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac{str(fac).replace(".", "_")}')


    # ais_Kca Iteration
    sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                       ais_ca = 100,ais_Kca = 5*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                       na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                       na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                       params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                       pfx=f'WT_ais_Kca{str(fac).replace(".", "_")}', update=True)
    sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac{str(fac).replace(".", "_")}')

    sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                    na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                    na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_KP{str(fac).replace(".", "_")}', update=True)
    sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac{str(fac).replace(".", "_")}')
        



# soma_na12 Iteration
    sim_test_soma_na12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5*fac, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_soma_na12{str(fac).replace(".", "_")}', update=True)
    sim_test_soma_na12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na12_fac{str(fac).replace(".", "_")}')

    # soma_na16 Iteration
    sim_test_soma_na16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1*fac, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_soma_na16{str(fac).replace(".", "_")}', update=True)
    sim_test_soma_na16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'soma_na16_fac{str(fac).replace(".", "_")}')

    
    sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3*fac,nav16=7.5, somaK=1, KP=1000, KT=10,
                                     ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                     pfx=f'WT_nav12_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac{str(fac).replace(".", "_")}')

    # nav16 Iteration
    sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5*fac, somaK=1, KP=1000, KT=10,
                                     ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                     pfx=f'WT_nav16_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac{str(fac).replace(".", "_")}')

    

    sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*fac,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                              ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                              na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                              na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                              params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav12_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac{str(fac).replace(".", "_")}')

    # ais_nav16_fac Iteration
    sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*fac,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                            ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                            na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                            na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                            params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav16_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac{str(fac).replace(".", "_")}')




# somaK Iteration
    sim_test_somaK = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1*fac, KP=1000, KT=10,
                                     ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                     na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                     na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                     params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                     pfx=f'WT_somaK_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_somaK.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'somaK_fac{str(fac).replace(".", "_")}')

    # KT Iteration
    sim_test_KT = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10*fac,
                                  ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                  na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                  na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                  params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                  pfx=f'WT_KT_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_KT.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KT_fac{str(fac).replace(".", "_")}')

    # ais_ca Iteration
    sim_test_ais_ca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                      ais_ca = 100*fac,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                      na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                      na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                      params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                      pfx=f'WT_ais_ca_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_ais_ca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_ca_fac{str(fac).replace(".", "_")}')

    # ais_Kca Iteration
    sim_test_ais_Kca = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                       ais_ca = 100,ais_Kca = 5*fac, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na=1,
                                       na12name='na12_HMM_TEMP_PARAMS',mut_name='na12_HMM_TEMP_PARAMS',na12mechs=['na12','na12mut'],
                                       na16name='na16_HMM_TEMP_PARAMS',na16mut_name='na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                       params_folder='./params/', plots_folder=f'{root_path_out}/', 
                                       pfx=f'WT_ais_Kca_fac{str(fac).replace(".", "_")}', update=True)
    sim_test_ais_Kca.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_Kca_fac{str(fac).replace(".", "_")}')
'''

'''   
        sim_test_ais_nav12_fac = tf.Na12Model_TF(ais_nav12_fac=2*fac,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                                ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                                params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav12_fac{str(fac).replace(".", "_")}', update=True)
        sim_test_ais_nav12_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav12_fac{str(fac).replace(".", "_")}')

        # ais_nav16_fac Iteration
        sim_test_ais_nav16_fac = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10*fac,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                                ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                                na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                                na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                                params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_ais_nav16_fac{str(fac).replace(".", "_")}', update=True)
        sim_test_ais_nav16_fac.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'ais_nav16_fac{str(fac).replace(".", "_")}')

        # nav12 Iteration
        sim_test_nav12 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3*fac,nav16=7.5, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_nav12{str(fac).replace(".", "_")}', update=True)
        sim_test_nav12.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav12_fac{str(fac).replace(".", "_")}')

        # nav16 Iteration
        sim_test_nav16 = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5*fac, somaK=1, KP=1000, KT=10,
                                        ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                        na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                        na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                        params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_nav16{str(fac).replace(".", "_")}', update=True)
        sim_test_nav16.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'nav16_fac{str(fac).replace(".", "_")}')

        # KP Iteration
        sim_test_KP = tf.Na12Model_TF(ais_nav12_fac=2,ais_nav16_fac=10,nav12=3,nav16=7.5, somaK=1, KP=1000, KT=10,
                                    ais_ca = 100,ais_Kca = 5, soma_na12=2.5, soma_na16=1, dend_nav12=1, node_na = 1,
                                    na12name = 'na12_HMM_TEMP_PARAMS',mut_name = 'na12_HMM_TEMP_PARAMS',na12mechs = ['na12','na12mut'],
                                    na16name = 'na16_HMM_TEMP_PARAMS',na16mut_name = 'na16_HMM_TEMP_PARAMS',na16mechs=['na16','na16mut'],
                                    params_folder = './params/', plots_folder = f'{root_path_out}/', pfx=f'WT_KP{str(fac).replace(".", "_")}', update=True)
        sim_test_KP.wtvsmut_stim_dvdt(wt_Vm=wt_Vm1,wt_t=wt_t1,sim_config=sim_config_soma,vs_amp=[0.5], fnpre=f'KP_fac{str(fac).replace(".", "_")}')
        

'''
















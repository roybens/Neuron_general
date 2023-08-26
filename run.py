import Developing_12HMM as Dev
import matplotlib.pyplot as plt
import numpy as np
import NrnHelper as NH
import Na12ModelGY as Mature
from currentscape.currentscape import plot_currentscape



models= ['5may','6July_1','0208','0407','0607','0708','0906','0908_9','0908','0908g','1008','1107_11july','1207','1807','2407','3107','old','tauless_2002','tauless2000','UDB']
#sim = Dev.Developing_12HMM(na12name = 'na12_R850P_old', mut_name = 'na12_R850P_old' , na16name = 'na12_R850P_old' , mut16_name = 'na12_R850P_old')
#sim.plot_crazy_stim('syn_stim.csv',stim_duration=0.2)

# Currentscape 
sim_config = {
                'section' : 'soma',
                'segment' : 0.5,
                'section_num': 0,
                'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'],
                'ionic_concentrations' :["cai", "ki", "nai"]
                
            }



for i in range(20):
    current_names = sim_config['currents']
    current_model = models[i]
    plot_config = {
        "output": {
            "savefig": True,
            "dir": "./Plots/Currentscape/",
            "fname": f"Dev_{current_model}_60mV",
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
    current_model = f'na12_R850P_{current_model}'
    sim = Dev.Developing_12HMM(na12name = current_model, mut_name =current_model , na16name = current_model , mut16_name = current_model)
    Vm, I, t, stim, ionic = sim.make_current_scape(sim_config=sim_config)
    plot_currentscape(Vm, [I[x] for x in I.keys()], plot_config,[ionic[x] for x in ionic.keys()])
    
"""
# Get FI data for each Model, and add to the list p 
p=[]
for i in range(20):
    current_model = models[i]
    current_model = f'na12_R850P_{current_model}'
    sim = Dev.Developing_12HMM(na12name = current_model, mut_name =current_model , na16name = current_model , mut16_name = current_model)
    p.append(sim.plot_fi_curve(0,1,10,fn = f'{models[i]}_fi'))
    print(p)

# FI data of homozygous models with Roy's ionic changes 

WT= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#nav12 = 3.5    nav16 = 1.2     ais_Kca = 0.03*ais_Kca  ais_ca = 0.04*ais_ca    KP=1.1*KP   K = 3*K     KT = 0.025*0.5*KT
               
model_nAP = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 2, 4, 5, 7, 9, 10, 11],[0, 0, 0, 0, 0, 4, 7, 10, 12, 15],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            
###################################################################### FI data of homozygous models with my ionic changes #####################################################

#nav12 = 3.5    nav16 = 1.2     ais_Kca = 0.03*ais_Kca  ais_ca = 0.04*ais_ca    KP=.1*KP   K = 1*K     KT = 0.025*0.5*KT
WT = [0, 0, 0, 0, 0, 0, 0, 1, 1, 2]
nAP= [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 2, 5], 
            [0, 0, 0, 0, 1, 1, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 2, 4, 5, 6, 7, 9, 9, 10], [0, 0, 0, 3, 6, 9, 11, 14, 14, 15], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 1, 1],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

      
models= ['5may','6July_1','0208','0407','0607','0708','0906','0908_9','0908','0908g','1008','1107_11july','1207','1807','2407','3107','old','tauless_2002','tauless2000','UDB']

######################################################################      Plot all FI curves in one plot       #####################################################

x=[]

for k in range (1,11):
    x.append((k-1)*1/9)
    
fig, ax = plt.subplots()

for j in range(20):
    rel_nAP = [a - b for a, b in zip(nAP[j], WT)]
    y= rel_nAP
    if nAP[j]==[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        ax.plot(x, y,'go-', label=f'{models[j]}')
    elif nAP[j]==[0, 0, 0, 0, 0, 0, 0, 1, 1, 1]:
        ax.plot(x,y, 'ro-', label= f'{models[j]}')         
    else:
        ax.plot(x, y)
        label = models[j]
        ax.annotate(label,
        xy     = (     x[-1], y[-1]),
        xytext = (1.1*x[-1],y[-1]))
    
plt.legend()
plt.ylabel('nAPs for 500ms epoch')
plt.xlabel('Stim [nA]')
plt.savefig(f'Developing models all ionic edition relative')  


"""

















"""

    
#fig_volts,axs_volts = plt.subplots(1,figsize=(8,7.8))

#sim.plot_stim(axs = axs_volts,dt=0.01,stim_amp = 0.4,rec_extra = True,plot_fn = 'na12_V1282F_stim',stim_dur = 500)

#Mature_models
na12_R850P_0208 =[0, 0, 5, 11, 14, 19, 24, 26, 29, 32]
na12_R850P_0908g=[0, 0, 5, 10, 14, 19, 24, 27, 30, 32]
na12_R850P_1107_11july= [0, 0, 6, 12, 16, 21, 25, 28, 31, 34]
na12_R850P_1807=[0, 0, 6, 11, 17, 21, 25, 28, 31, 34]
na12_R850P_3107=[0, 0, 6, 11, 15, 19, 24, 27, 30, 32]
na12_R850P_old=[0, 0, 6, 11, 16, 23, 27, 31, 34, 36]
WT=[0, 0, 5, 11, 14, 19, 25, 28, 31, 34]


# Developing models
na12_R850P_0208 =[0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
na12_R850P_0908g= [0, 0, 0, 0, 0, 0, 1, 1, 2, 3]
na12_R850P_1107_11july= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
na12_R850P_1807= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
na12_R850P_3107=[0, 0, 3, 6, 9, 11, 14, 15, 17, 18]
na12_R850P_old=[0, 0, 0, 3, 9, 15, 19, 22, 24, 26]
WT=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1]






Stimul=[]

for i in range (1,11):
    Stimul.append((i-1)*1/9)
    
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

for i in range(20)

plt.plot(Stimul, na12_R850P_0208, label='0208')
plt.plot(Stimul, na12_R850P_0908g, label='0908g')
plt.plot(Stimul, na12_R850P_1107_11july, label='1107_11july')
plt.plot(Stimul, na12_R850P_1807, label='1807')
plt.plot(Stimul, na12_R850P_3107, label='3107')
plt.plot(Stimul, na12_R850P_old, label='old')
plt.plot(Stimul, WT, label='WT')
plt.ylabel('nAPs for 500ms epoch')
plt.xlabel('Stim [nA]')
plt.legend()
plt.savefig(f'Developing models top6')  



"""

#Dev4 is the homozygous with 4 alleles with mutation, Dev 2 is heterozygous, all with ionic changes, Dev42:without ionic changes
#'na12_R850P_0208' hom:[0, 0, 5, 11, 14, 19, 24, 26, 29, 32],       without Roy ionic changes: [0, 1, 3, 7, 10, 14, 18, 21, 23, 26], Dev4: [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
#'na12_R850P_0908g' hom:[0, 0, 5, 10, 14, 19, 24, 27, 30, 32],      without Roy ionic changes: [0, 1, 3, 7, 10, 14, 18, 21, 23, 26], Dev4: [0, 0, 0, 0, 0, 0, 1, 1, 2, 3]
#'na12_R850P_1107_11july' hom:[0, 0, 6, 12, 16, 21, 25, 28, 31, 34],without Roy ionic changes: [0, 1, 3, 8, 12, 16, 19, 23, 25, 28],  Dev 4 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],Dev2: [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
#'na12_R850P_1107_11july' hom dt=0.01 :[0, 0, 6, 12, 16, 21, 25, 28, 31, 34]                 :                          
#'na12_R850P_1807' hom: [0, 0, 6, 11, 17, 21, 25, 28, 31, 34],      without Roy ionic changes: [0, 1, 3, 8, 11, 15, 19, 22, 25, 28], Dev4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#'na12_R850P_3107' hom: [0, 0, 6, 11, 15, 19, 24, 27, 30, 32],      without Roy ionic changes: [0, 1, 3, 7, 10, 15, 18, 21, 23, 26], Dev4: [0, 0, 3, 6, 9, 11, 14, 15, 17, 18], [0, 0, 2, 3, 6, 8, 9, 11, 12, 13]
#'na12_R850P_old' hom[0, 0, 6, 11, 16, 23, 27, 31, 34, 36],         without Roy ionic changes: [0, 1, 3, 8, 12, 16, 21, 23, 26, 29], Dev4: [0, 0, 0, 3, 9, 15, 19, 22, 24, 26]
#WT:[0, 0, 5, 11, 14, 19, 25, 28, 31, 34],                          without Roy ionic changes: [0, 1, 3, 7, 10, 15, 18, 21, 24, 26], Dev4: [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
#sim = Mature.Na12ModelGY(na12name ='na12_orig1', mut_name ='na12_R850P_V1282F')

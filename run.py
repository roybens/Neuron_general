import Developing_12HMM as Dev
import matplotlib.pyplot as plt
import numpy as np
import NrnHelper as NH
import Na12ModelGY as Mature
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


#list of all models
models= ['5may','6July_1','0208','0407','0607','0708','0906','0908_9','0908','0908g','1008','1107_11july','1207','1807','2407','3107','old','tauless_2002','tauless2000','UDB']

i=19
current_model = models[i]
current_model = f'na12_R850P_{current_model}'
sim = Dev.Developing_12HMM(na12name = current_model, mut_name =current_model , na16name = current_model , mut16_name = current_model)
p=sim.plot_fi_curve(0,1,10,fn = f'fi_{models[i]}_hom')

WT= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model0= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model1= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model2= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model3= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model4= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model5= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model6= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model7= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model8= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model9= [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]      #0908g
model10= [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]     #1008
model11= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model12= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model13= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model14= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
model15= [0, 0, 0, 2, 4, 5, 7, 9, 10, 11]   #3107
model16= [0, 0, 0, 0, 0, 4, 7, 10, 12, 15]  #old
model17= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     
model18= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     
model19= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


#fig_volts,axs_volts = plt.subplots(1,figsize=(8,7.8))

#sim.plot_stim(axs = axs_volts,dt=0.01,stim_amp = 0.4,rec_extra = True,plot_fn = 'na12_V1282F_stim',stim_dur = 500)
"""
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



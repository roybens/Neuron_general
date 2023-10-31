from NeuronModelClass import NeuronModel
from NrnHelper import *
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import numpy as np
import csv

class na12HH16HMM_TF:
    # def __init__(self,na12name = 'na12_TF2',mut_name= 'na12_TF2',  na12mechs = ['na12','na12_mut'],na16name = 'na16_orig2', na16mechs = ['na16','na16_mut'], params_folder = './params/HOF_params_JSON/',
    #     nav12=1,nav16=1,K=1,KT=1,KP=1,somaK=1,ais_ca = 1,ais_Kca = 1,soma_na16=1,soma_na12 = 1,node_na = 1,plots_folder = f'./Plots/12HH16HMM_TF/mut/'):
    def __init__(self, na12mechs = ['na12','na12_mut'],na16name = 'na16mut44_092623_vshiftPLUS10',na16mut = 'na16MORAN_100223', na16mechs = ['na16','na16mut'], params_folder = './params/',
        nav12=1,nav16=1,K=1,KT=1,KP=1,somaK=1,ais_ca = 1,ais_Kca = 1,soma_na16=1,soma_na12 = 1,node_na = 1,plots_folder = f'./Plots/12HH16HMM_TF/103123/Mut_currents_vshiftplus10/'):
    

        #na16mut44_092623_vshiftPLUS10     currents_vshiftplus10
        
        ###########ais_Kca = 0.5
        # #K = 0.6
        # #update_param_value(self.l5mdl,['SKv3_1'],'vtau',25)
        # #ais_ca = 2
        # #soma_na16 = 0.7
        # #soma_na12 = 0.7
        # #nav12 = 3
        # #nav16 = 1
        # #KP = 0.1
        # #somaK = 2
        # #KP=3
        # #K=3
        # #KT = 0.5
        
        # #nav12 = 1.2
        # #nav16 = 1.2
        
        # #______________M1TTPC2
        # #nav12 = 3.5
        # #nav12 = 5 #Tim#######################
        # #nav16 = 1.2
        # # ais_Kca = 0.03*ais_Kca
        # # ais_ca = 0.04*ais_ca
        # # KP=1.1*KP
        # # K = 4.8*K
        # # KT = 0.025*0.5*KT

        # #___________________TTPC_M1_Na_HH.py from M1_TTPC2 branch
        # #ais_Kca = 0.03*ais_Kca
        # #K = 0.6
        # #update_param_value(self.l5mdl,['SKv3_1'],'vtau',25)
        ###########ais_ca = 0.04*ais_ca
        # #soma_na16 = 0.7
        # #soma_na12 = 0.7
        # #nav12 = 1.8 *nav12
        # #nav16 = 1.8 *nav16#the wt should be 1.1 and then add to that what we get from the input
        nav12 = 3.25
        # #nav16 = 1.1*nav16
        ###########KP = 1.2*KP
        ###########somaK = 0.5 * somaK
        # KP=0.95*KP
        ###########K = 4.8*K
        ###########KT = 0.025*0.5*KT
        # #nav12 = 1.2
        #nav16 = 5
        
       #______________GY
        #KP= KP
        
    

        self.l5mdl = NeuronModel(nav12=nav12, nav16=nav16,axon_K = K,axon_Kp = KP,axon_Kt = KT,soma_K = somaK,ais_ca = ais_ca,ais_KCa=ais_Kca,soma_nav16=soma_na16,soma_nav12 = soma_na12,node_na = node_na)
        update_param_value(self.l5mdl,['SKv3_1'],'mtaumul',6)
   
        self.mut_mech = [na12mechs[1]]  #new from Namut: different parameters for the wt and mut mechanisms
        self.wt_mech = [na12mechs[0]]   #new from Namut
        #self.na16mechs = na16mechs
        
        
        self.wt_mech16 = [na16mechs[0]]   #TF adding ability to control na16 params (WT, het, hom)
        self.mut_mech16 = [na16mechs[1]]

        self.plot_folder = plots_folder 
        self.plot_folder = f'{plots_folder}'
        Path(self.plot_folder).mkdir(parents=True, exist_ok=True)

     #this model originally makes het but if you put wt name as mut name it creates the WT and if you put mut name as
     #na12 name and mut_name then you will have homozygus
        self.l5mdl.h.working()

        ###______Commented the following lines to not use na12 params

        # p_fn_na12 = f'{params_folder}{na12name}.txt'  
        # p_fn_na12_mech = f'{params_folder}{mut_name}.txt'
        # print(f'using wt_file {na12name}')
        # self.na12_p = update_mech_from_dict(self.l5mdl, p_fn_na12, self.wt_mech) 
        # print(f'using mut_file {mut_name}')
        # self.na12_pmech = update_mech_from_dict(self.l5mdl, p_fn_na12_mech, self.mut_mech)
        
        print(f'using na16_file {na16name}')
        p_fn_na16 = f'{params_folder}{na16name}.txt'
        self.na16_p = update_mech_from_dict(self.l5mdl, p_fn_na16, self.wt_mech16)
        print(f'using na16_mut_file {na16mut}')
        p_fn_na16mut = f'{params_folder}{na16mut}.txt'
        self.na16_pmut = update_mech_from_dict(self.l5mdl, p_fn_na16mut, self.mut_mech16)

        
    def make_current_scape(self, sim_config = {
                        'section' : 'soma',
                        'segment' : 0.5,
                        'section_num': 0,
                        #'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'],
                        'currents' : ['ina','ica','ik'],
                        'ionic_concentrations' :["cai", "ki", "nai"]
                        
                    }):

        self.l5mdl.init_stim(amp=0.5,sweep_len = 500)
        Vm, I, t, stim, ionic = self.l5mdl.run_sim_model(dt=0.01,sim_config=sim_config) #change time steps here
        return Vm, I, t, stim, ionic
    
    #__________added this function to get overexp and ttx to work   
    def make_mut(self,mut_mech16,p_fn_na16mut): 
        print(f'updating mut {mut_mech16} with {p_fn_na16mut}')
        self.na16_p_mut = update_mech_from_dict(self.l5mdl, p_fn_na16mut, self.mut_mech16)

    def update_gfactor(self,gbar_factor = 1):
        update_mod_param(self.l5mdl, self.mut_mech, gbar_factor, gbar_name='gbar')

    def plot_stim(self,stim_amp = 0.5,dt = 0.02,clr = 'black',plot_fn = 'step',axs = None,rec_extra = False, stim_dur = 500):
        self.dt = dt
        if not axs:
            fig,axs = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        self.l5mdl.init_stim(stim_dur = stim_dur, amp=stim_amp )
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
        file_path_to_save=f'{self.plot_folder}{plot_fn}.pdf'
        plt.savefig(file_path_to_save, format='pdf')
        return axs
    
    def plot_crazy_stim(self, stim_csv, stim_duration = 0.2, dt = 0.1): # physiological (noisy) stimulation 
        self.dt = dt
        #Read CSV file for stimulation amplitudes and add the to amplitude list
        amplitudes = []
        v_m = []
        t_m = []
        with  open(stim_csv, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                ampl = float(row[0])
                amplitudes.append(ampl)
                
        #Create an empty plot        
        fig,axs = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
             
        #Stimulate the models with amplitudes at fix time points (every 0.2 ms)
        stim_start = 100
        for ampl in amplitudes:
            self.l5mdl.init_stim(sweep_len = 800, stim_start = stim_start , stim_dur = stim_duration, amp = ampl)
            Vm, I, t, stim = self.l5mdl.run_model(dt=dt) 
            self.volt_soma = Vm
            self.I = I
            self.t = t
            self.stim = stim
            stim_start = t
            v_m.append(Vm)
            t_m.append(t)
            
        axs.plot(t_m,v_m, label='Vm', color=clr,linewidth=1)
        axs.locator_params(axis='x', nbins=5)
        axs.locator_params(axis='y', nbins=8)
        file_path_to_save=f'{self.plot_folder}{plot_crazy_stim}.pdf'
        plt.savefig(file_path_to_save, format='pdf')
        
        return axs
        
            
    def plot_currents(self,stim_amp = 1,dt = 0.01,clr = 'black',plot_fn = 'Na16mut_vsh_1_150ms',axs = None, stim_dur = 500):
        if not axs:
            fig,axs = plt.subplots(4,figsize=(cm_to_in(8),cm_to_in(30)))
        self.l5mdl.init_stim(stim_dur = stim_dur, amp=stim_amp,sweep_len = 150) #sweep_len = time in ms?
        Vm, I, t, stim = self.l5mdl.run_model(dt=dt)
        axs[0].plot(t,Vm, label='Vm', color=clr,linewidth=1)
        axs[0].locator_params(axis='x', nbins=5)
        axs[0].locator_params(axis='y', nbins=8)
        
        axs[1].plot(t,I['Na'],label = 'Na',color = 'red')
        axs[2].plot(t,I['K'],label = 'K',color = 'black')
        axs[3].plot(t,I['Ca'],label = 'Ca',color = 'green')
        #add_scalebar(axs)
        file_path_to_save=f'{self.plot_folder}Ktrials2_{plot_fn}.pdf'
        plt.savefig(file_path_to_save+'.pdf', format='pdf', dpi=my_dpi)
        return axs
    
    def get_axonal_ks(self, start_Vm = -72, dt= 0.1,rec_extra = False):
        h.dt=dt
        self.dt = dt
        h.finitialize(start_Vm)
        timesteps = int(h.tstop/h.dt)

        Vm = np.zeros(timesteps)
        I = {}
        I['Na'] = np.zeros(timesteps)
        I['K'] = np.zeros(timesteps)
        I['K31'] = np.zeros(timesteps)
        I['KT'] = np.zeros(timesteps)
        I['KCa'] = np.zeros(timesteps)
        I['KP'] = np.zeros(timesteps)
        stim = np.zeros(timesteps)
        t = np.zeros(timesteps)

        for i in range(timesteps):
            Vm[i] = h.cell.soma[0].v
            I['Na'][i] = self.l5mdl.ais(0.5).ina
            I['K'][i] = self.l5mdl.ais(0.5).ik
            I['K31'][i] = self.l5mdl.ais.gSKv3_1_SKv3_1
            I['KP'][i] = self.l5mdl.ais.gK_Pst_K_Pst
            I['KT'][i] = self.l5mdl.ais.gK_Tst_K_Tst
            I['KCa'][i] = self.l5mdl.ais.gSK_E2_SK_E2
            t[i] = i*h.dt / 1000
            stim[i] = h.st.amp
            h.fadvance()
        return Vm, I, t, stim


    def plot_axonal_ks(self,stim_amp = 0.5,dt = 0.01,clr = 'black',plot_fn = 'step_axon_ks',axs = None, stim_dur = 500):
        if not axs:
            fig,axs = plt.subplots(7,2,figsize=(cm_to_in(16),cm_to_in(70)))
        self.l5mdl.init_stim(stim_dur = stim_dur, amp=stim_amp,sweep_len = 500)
        Vm, I, t, stim = self.get_axonal_ks(dt=dt)
        axs[0][0].plot(t,Vm, label='Vm', color=clr,linewidth=1)
        plot_dvdt_from_volts(Vm,self.dt,axs[0][1])
        axs[0][0].locator_params(axis='x', nbins=5)
        axs[0][0].locator_params(axis='y', nbins=8)
        
        axs[1][0].plot(t,I['Na'],label = 'Na',color = 'red')
        axs[1][0].legend()
        plot_dg_dt(I['Na'],Vm,self.dt,axs[1][1])
        axs[2][0].plot(t,I['K'],label = 'K',color = 'black')
        plot_dg_dt(I['K'],Vm,self.dt,axs[2][1])
        axs[2][0].legend()
        axs[3][0].plot(t,I['K31'],label = 'K31',color = 'green')
        plot_dg_dt(I['K31'],Vm,self.dt,axs[3][1])
        axs[3][0].legend()
        axs[4][0].plot(t,I['KP'],label = 'KP',color = 'orange')
        plot_dg_dt(I['KP'],Vm,self.dt,axs[4][1])
        axs[4][0].legend()
        axs[5][0].plot(t,I['KT'],label = 'KT',color = 'yellow')
        plot_dg_dt(I['KT'],Vm,self.dt,axs[5][1])
        axs[5][0].legend()
        axs[6][0].plot(t,I['KCa'],label = 'KCa',color = 'grey')
        plot_dg_dt(I['KCa'],Vm,self.dt,axs[6][1])
        axs[6][0].legend()
        



        #add_scalebar(axs)
        #file_path_to_save=plot_fn
        file_path_to_save=plot_fn
        plt.savefig(file_path_to_save, format='pdf', dpi=my_dpi)
        return axs
        
    def plot_fi_curve(self,start,end,nruns,wt_data = None,ax1 = None, fig = None,fn = 'ficurve'): #start=0,end=0.6,nruns=14
        fis = get_fi_curve(self.l5mdl,start,end,nruns,dt = 0.1,wt_data = wt_data,ax1=ax1,fig=fig,fn=f'{self.plot_folder}{fn}.pdf')
        return fis
    
    
    

    def plot_volts_dvdt(self,stim_amp = 0.5):
        fig_volts,axs_volts = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        fig_dvdt,axs_dvdt = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        self.plot_stim(axs = axs_volts,dt=0.02)
        plot_dvdt_from_volts(self.volt_soma,self.dt,axs_dvdt)
        file_path_to_save=f'{self.plot_folder}AnnaModel_volts_dvdt_{stim_amp}.pdf'
        fig_dvdt.savefig(file_path_to_save, format='pdf', dpi=my_dpi)
        file_path_to_save=f'{self.plot_folder}AnnaModel_volts_{stim_amp}.pdf'
        fig_volts.savefig(file_path_to_save, format='pdf', dpi=my_dpi)


    def get_ap_init_site(self):
        self.plot_stim(stim_amp = 0.5,rec_extra=True)
        soma_spikes = get_spike_times(self.volt_soma,self.t)
        axon_spikes = get_spike_times(self.extra_vms['axon'],self.t)
        ais_spikes = get_spike_times(self.extra_vms['ais'],self.t)
        for i in range(len(soma_spikes)):
            print(f'spike #{i} soma - {soma_spikes[i]}, ais - {ais_spikes[i]}, axon - {axon_spikes[i]}')

    
    ##_______________________Added to enable run of TTX and overexpression functions
    def plot_model_FI_Vs_dvdt(self,vs_amp,fnpre = '',wt_fi = None, start=0,end=2,nruns=21):
        
        #______________________na16 1.1 factor_______________________________________________________
        #wt_fi = [0, 0, 7, 10, 13, 16, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 33]#wt1.4, mut1, added make_mut
        #wt_fi = [0, 2, 7, 11, 15, 17, 19, 20, 22, 23, 25, 26, 27, 28, 29, 29, 31, 32, 33, 34, 35]#wt2.4, mutNONE, 
        #wt_fi = [0, 2, 7, 11, 15, 17, 19, 20, 22, 23, 25, 26, 27, 28, 29, 29, 31, 32, 33, 34, 35]#wt2.4, mut0
        #wt_fi = [0, 0, 7, 10, 13, 16, 18, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 31, 32, 33]#wt1, mut1.4
        #wt_fi = [0, 0, 7, 10, 14, 16, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 33]#wt1.2, mut1.4
        #_____________________________________________________________________________________________

        #_______________________FIXED! by taking away 1.1 factor______________________________________
        #wt_fi = [0, 2, 7, 11, 14, 17, 18, 20, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 34] #wt2.4, mut0, nav16=1 (not 1.1*nav16) 120%WT
        #wt_fi = [0, 2, 7, 11, 14, 17, 18, 20, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 34] #wt1.4, mut 1
        #wt_fi = [0, 0, 5, 9, 12, 14, 17, 18, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 31, 32] #100% wt, wt1, mut1
        #wt_fi = [0, 0, 0, 1, 5, 8, 10, 12, 14, 16, 17, 18, 20, 21, 22, 22, 23, 24, 25, 25, 26] #20% WT, wt.4, mut0
        #_____________________________________________________________________________________________


        #_______________________100523________________________________________________________________
        #wt_fi = [0, 0, 5, 10, 12, 15, 17, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 31, 32] #100%WT, wt2, mut0
        #wt_fi = [0, 1, 6, 10, 13, 15, 17, 20, 20, 22, 23, 24, 26, 27, 28, 29, 29, 30, 31, 32, 33] #120% WT, wt2.4, mut0
        #wt_fi = [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 7, 9, 9, 10] #100% G1625R, wt0, mut2
        #wt_fi = [0, 0, 0, 1, 5, 8, 10, 12, 14, 16, 17, 18, 20, 21, 22, 22, 23, 24, 25, 25, 26] #20% WT, wt.4, mut0
        #_____________________________________________________________________________________________

               
        #_______________Kaustubh's Params no modifiers_______________________________________________
        #wt_fi = [0, 0, 7, 12, 16, 19, 21, 23, 25, 26, 27, 28, 29, 30, 31, 32, 32, 34, 34, 35, 36] #100%WT
        #wt_fi = [0, 1, 8, 14, 17, 19, 21, 24, 24, 26, 27, 28, 30, 30, 31, 32, 33, 34, 35, 36, 37] #120% WT
        
        #____________________Kaustubh + Tim Params Na16 paper first round__________________________________
        #wt_fi = [0, 0, 6, 10, 14, 16, 18, 20, 21, 23, 24, 25, 26, 28, 29, 29, 30, 31, 32, 33, 33] #100%WT
        wt_fi = [0, 1, 6, 11, 14, 16, 18, 20, 22, 23, 24, 26, 27, 28, 29, 30, 31, 31, 32, 33, 34] #120%WT
        #wt_fi = [0, 0, 0, 1, 5, 8, 11, 13, 15, 16, 17, 19, 20, 21, 22, 22, 23, 24, 25, 25, 26] #20%WT
        
        #____________________103023 +200% G1625R raw data____________________________________________________________
        #wt_fi =  [0, 0, 4, 8, 12, 15, 17, 19, 21, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35] 100%WT + 20%(40%)G1625R
        #wt_fi = [0, 0, 2, 5, 9, 12, 14, 16, 18, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 31]50%WT + 50%(100%) G1625R
        #wt_fi = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3] 20%(40%)G1625R
        #___________________________________________________________________________________________________




        for curr_amp in vs_amp:
            #fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(3),cm_to_in(3.5)))
            # fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9),cm_to_in(10.5)))
            # axs[0] = self.plot_stim(axs = axs[0],stim_amp = curr_amp,dt=0.01)
            # #axs[0] = self.plot_stim(axs = axs[0],stim_amp = curr_amp,dt=0.05)
            # axs[1] = plot_dvdt_from_volts(self.volt_soma,self.dt,axs[1])
            # add_scalebar(axs[0])
            # add_scalebar(axs[1])
            # fn = f'{self.plot_folder}/{fnpre}dvdt_vs_{curr_amp}.pdf'
            # fig_volts.savefig(fn)
            csv_volts = f'{self.plot_folder}/{fnpre}vs_{curr_amp}.csv'
            
            ###
            #self.plot_volts_dvdt(stim_amp = curr_amp)

            fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
            self.plot_stim(axs = axs[0],stim_amp = curr_amp,dt=0.005)
            plot_dvdt_from_volts(self.volt_soma,self.dt,axs[1])
            fn2 = f'{self.plot_folder}/{fnpre}{curr_amp}.pdf'
            fig_volts.savefig(fn2)
            ###


            with open(csv_volts, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Voltage'])  # Write header row
                writer.writerows(zip(self.volt_soma))
        
        self.plot_fi_curve_2line(start,end,nruns, wt_data=wt_fi, fn = fnpre + '_fi')
        fi_ans = self.plot_fi_curve_2line(start,end,nruns,wt_data = wt_fi,fn = fnpre + '_fi')
        with open(f'{self.plot_folder}/{fnpre}.csv', 'w+', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(fi_ans)
        return fi_ans
    ##_________________________________________________________________________________________________
    def plot_fi_curve_2line(self,start,end,nruns,wt_data=None,ax1 = None, fig = None,fn = 'ficurve'): #start=0,end=0.6,nruns=14 (change wt_data from None to add WT line)
        fis = get_fi_curve(self.l5mdl,start,end,nruns,dt = 0.1,wt_data = wt_data,ax1=ax1,fig=fig,fn=f'{self.plot_folder}{fn}.pdf')
        print()
        return fis
    
####____________________Overexpression and TTX code from Roy's M1TTPC branch from 16HMMtau.py
def overexp(na16name,na16mut, plots_folder, wt_fac,mut_fac,plot_wt=False,fnpre = '100WT20G1625R',axon_KP = 1, na16mechs =['na16','na16mut']):
    sim = na12HH16HMM_TF(nav16 = wt_fac,KP=axon_KP, na16name=na16name,na16mut=na16mut, plots_folder = plots_folder,params_folder = './params/', na16mechs=na16mechs)
    if plot_wt:
        wt_fi = sim.plot_model_FI_Vs_dvdt([0.5,1,2],fnpre=f'{fnpre}_FI_') #Even if change mut_fac/wt_fac, will use old na16mut mech params since mut not updated
        #wt_fi = sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2,2.5,3],fnpre=f'{fnpre}_FI_')
    else:
        wt_fi = []
    print(f'wt_fi is {wt_fi}')
    if mut_fac:
        sim.make_mut(na16mechs[1],'./params/na16MORAN_100223.txt') #updates mech (Arg[1]) with new mod params dict (Arg[2])
        print('making mut')
        update_mod_param(sim.l5mdl,['na16mut'], mut_fac) #Adds multiplier to updated mod/mech parameters
        print('updated mod params')
        sim.l5mdl.h.finitialize()
        if plot_wt:
            sim.plot_model_FI_Vs_dvdt([0.5,1,2],wt_fi = wt_fi,fnpre=f'{fnpre}mutX{mut_fac}_')
            #sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2],wt_fi = wt_fi,fnpre=f'{fnpre}mutX{mut_fac}_')

        else:
            #sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2],fnpre=f'{fnpre}mutX{mut_fac}_')
            sim.plot_model_FI_Vs_dvdt([0.5,1,2],fnpre=f'{fnpre}mutXtest{mut_fac}_')

    else:
        #sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2],fnpre=f'{fnpre}_{mut_fac}_')
        ##sim.plot_model_FI_Vs_dvdt([0.5,1],fnpre=f'{fnpre}_{mut_fac}_else')
        return



def ttx(na16name,na16mut,plots_folder,wt_factor,mut_factor,fnpre = 'mut_TTX',axon_KP = 1):
    sim = na12HH16HMM_TF(KP=axon_KP,nav12=0, na16name=na16name, na16mut=na16mut, plots_folder = plots_folder)
    # if mut_factor>0:
    #     sim.make_mut('na16mut','na16mut44_092623.txt')
    update_mod_param(sim.l5mdl,['na16'],wt_factor)
    update_mod_param(sim.l5mdl,['na16mut'],mut_factor)
    update_mod_param(sim.l5mdl,['na12','na12mut'],0,print_flg = True)
    
    #make_currentscape_plot(fn_pre=fnpre,sim_obj = sim.l5mdl)
    # sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2],fnpre=f'{fnpre}WT_{wt_factor*100}_Mut_{mut_factor *100}_')
    sim.plot_model_FI_Vs_dvdt([1],fnpre=f'{fnpre}WT_{wt_factor*100}_Mut_{mut_factor *100}_') #only plot 1nA rather than range of amps


####____________________________________________________________________________________________    

def scan12_16(na16name, na16mut, plots_folder):
    #i12 = 1
    #i16 = 1
    for i12 in np.arange(3,1,-1): #(2,0.4,-0.5)
        for i16 in np.arange(3,1,-1):
            sim = na12HH16HMM_TF(na16name=na16name, na16mut=na16mut, nav12=i12, nav16=i16, plots_folder = plots_folder) #TF added args to run from runModel12HH16HMM_TF.py script
            #sim.make_wt()
            fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
            sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
            plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
            fn = f'{sim.plot_folder}/vs_dvdt12_{i12}_16_{i16}.pdf'
            fig_volts.savefig(fn)

        
def scan_sec_na():
    for fac in np.arange(0.1,1,0.1):
        sim = na12HH16HMM_TF(soma_na16=fac,soma_na12=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Na16_{fac}_Na12_{fac}.pdf'
        fig_volts.savefig(fn)
        """
        sim = na12HH16HMM_TF(soma_na12=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Na12_{fac}.pdf'
        fig_volts.savefig(fn)

        sim = na12HH16HMM_TF(node_na=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/node_na_{fac}.pdf'
        fig_volts.savefig(fn)
        """


def scanK(na16name, na16mut, plots_folder): #TF added args to run from runModel12HH16HMM_TF.py script
    for i in np.arange(0.05,5,0.5): #(.1,5,.5)

        sim = na12HH16HMM_TF(ais_ca=i,na16name=na16name, na16mut=na16mut, plots_folder = plots_folder)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(10),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/ais_CA_{i}_.pdf'
        fig_volts.savefig(fn)
        
        sim = na12HH16HMM_TF(ais_Kca=i,na16name=na16name, na16mut=na16mut, plots_folder = plots_folder)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(10),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/ais_Kca_{i}_.pdf'
        fig_volts.savefig(fn)
       
        sim = na12HH16HMM_TF(K=i,na16name=na16name, na16mut=na16mut, plots_folder = plots_folder)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/K_{i}_.pdf'
        fig_volts.savefig(fn)
        
        sim = na12HH16HMM_TF(somaK=i,na16name=na16name, na16mut=na16mut, plots_folder = plots_folder)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/somaK_{i}_.pdf'
        fig_volts.savefig(fn)


        sim = na12HH16HMM_TF(KP=i,na16name=na16name, na16mut=na16mut, plots_folder = plots_folder)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Kp_{i}_.pdf'
        fig_volts.savefig(fn)


        sim = na12HH16HMM_TF(KT=i,na16name=na16name, na16mut=na16mut, plots_folder = plots_folder)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(10),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Kt_{i}_.pdf'
        fig_volts.savefig(fn)





def scanKv31():
    
    vtau_orig = 18.700
    vinf_orig = -46.560
    for i in np.arange(0,21,5):
        sim = na12HH16HMM_TF()
        update_param_value(sim.l5mdl,['SKv3_1'],'vtau',vtau_orig+i)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/kv31_shift_vtau_{i}_.pdf'
        fig_volts.savefig(fn)
        update_param_value(sim.l5mdl,['SKv3_1'],'vtau',vtau_orig)

        
        sim = na12HH16HMM_TF()
        update_param_value(sim.l5mdl,['SKv3_1'],'vinf',vinf_orig+i)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/kv31_shift_vinf_{i}_.pdf'
        fig_volts.savefig(fn)
        update_param_value(sim.l5mdl,['SKv3_1'],'vinf',vinf_orig)
    mtaumul_orig = 4
    for i in np.arange(0.1,1,0.2):
        sim = na12HH16HMM_TF()
        update_param_value(sim.l5mdl,['SKv3_1'],'mtaumul',mtaumul_orig +i)
        fn = f'{sim.plot_folder}/kv31_shift_mtaumul_{i}_.pdf'
        sim.plot_axonal_ks(plot_fn = fn)
    update_param_value(sim.l5mdl,['SKv3_1'],'mtaumul',mtaumul_orig)
        

def scanKT():
    vshift_orig = -10
    for i in np.arange(10,31,10):
        sim = na12HH16HMM_TF()
        update_param_value(sim.l5mdl,['K_Tst'],'vshift',vshift_orig+i)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/kT_vshift_{i}_.pdf'
        fig_volts.savefig(fn)
    update_param_value(sim.l5mdl,['K_Tst'],'vshift',vshift_orig)
def test_params():
    for i in range(1,9):
        na16_name = f'na16WT{i}'
        sim = na12HH16HMM_TF(na16name = na16_name)
        sim.plot_currents()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/default_na16_{i}.pdf'
        fig_volts.savefig(fn)

def default_model(al1 = 'na12_orig1', al2= 'na12_orig1', typ= ''):
    sim = na12HH16HMM_TF(al1,al2)
    #sim.plot_currents()
    fig_volts,axs = plt.subplots(1,figsize=(cm_to_in(16),cm_to_in(16)))
    sim.plot_stim(axs = axs,stim_amp = 0.7 ,dt=0.005, stim_dur = 500)
    axs.set_title(f'{al2}_{typ}')
    #plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
    fn = f'{sim.plot_folder}/default_na12HMM_{typ}.pdf'
    fig_volts.savefig(fn)


# The combination of two bellow Plots dvdt of allele combinations on top of each other and safe as file compare.pdf
# give the WT and Mutant param file as input, al1 is for WT
# yu don't need to run default anymore

def dvdt_all(al1 = 'na12_orig1', al2= 'na12_R850P_5may', stim_amp = 0.5, Typ = None, stim_dur = 500): #stim_amp = 0.5 #nA
    sim = na12HH16HMM_TF(al1,al2)
    
    if al1 == al2 and al1 == 'na12_orig1':
        Typ = 'WT'
    elif al1 == al2:
        Typ = 'Hom'
    else: 
        Typ = 'Het'

    fig_volts,axs = plt.subplots(1,figsize=(cm_to_in(16),cm_to_in(16)))
    sim.plot_stim(axs = axs, stim_amp = stim_amp ,dt=0.005, stim_dur = stim_dur )
    axs.set_title(f'stim: {stim_amp}nA for {stim_dur}ms , al1: {al1}, al2: {al2}', fontsize=9)
    fn = f'{sim.plot_folder}{Typ}_{stim_amp}_{stim_dur}.pdf'
    fig_volts.savefig(fn)
    dvdt = np.gradient(sim.volt_soma)/sim.dt
    v= sim.volt_soma
    return v, dvdt
    
def dvdt_all_plot(al1 = 'na12_orig1', al2= 'na12_R850P_5may',stim_amp = 0.5, stim_dur = 500):
    volt = [[],[],[]]
    dvdts = [[],[],[]]
    volt[0], dvdts[0] = dvdt_all(al2,al2,stim_amp = stim_amp,  stim_dur = stim_dur ) # Homozygous
    volt[1], dvdts[1] = dvdt_all(al1,al2,stim_amp = stim_amp,  stim_dur = stim_dur ) # Heterozygous
    volt[2], dvdts[2] = dvdt_all(al1,al1,stim_amp = stim_amp,  stim_dur = stim_dur ) # WT
    fig_volts,axs = plt.subplots(1,figsize=(cm_to_in(17),cm_to_in(17)))
    axs.plot(volt[0], dvdts[0], 'g', label=f'Homozygous')
    axs.plot(volt[1], dvdts[1], 'b', label=f'Heterozygous')
    axs.plot(volt[2], dvdts[2], 'r', label=f'WT')
    
    axs.set_xlabel('voltage(mV)',fontsize=9)
    axs.set_ylabel('dVdt(mV/s)',fontsize=9)
    axs.set_title(f'stim {stim_amp}, al1: {al1}, al2: {al2}', fontsize=9)
    axs.legend()
    fn = f'./Plots/Tim/{al2}_{stim_amp}_{stim_dur}.pdf'
    fig_volts.savefig(fn)





#    def make_mut(self,mut_mech16,p_fn_na16mut): 



#sim = na12HH16HMM_TF('na12_orig1', 'na12_orig1')
#sim.plot_currents()
#sim.get_ap_init_site()
#scan_sec_na()
#update_param_value(sim.l5mdl,['SKv3_1'],'mtaumul',1)
#sim.plot_volts_dvdt()
#sim.plot_fi_curve(0,1,10)
#default_model(al1 = 'na12_orig1',al2 = 'na12_orig1',typ='WT')
#scanK()
#scanKT()
#scanKv31()
#scan12_16()
##plot_mutant(na12name = 'na12_R850P',mut_name= 'na12_R850P')
#sim.plot_axonal_ks()
"""
for i in range (6,12):
    for j in range (1,3):
        dvdt_all_plot(al1 = 'na12_orig1', al2= 'na12_R850P_5may', stim_amp=i*0.05,  stim_dur = j* 500 )

for i in range (6,12):
    for j in range (1,3):
        dvdt_all_plot(al1 = 'na12_orig1', al2= 'na12_R850P_old', stim_amp=i*0.05,  stim_dur = j* 500 )
    
for i in range (6,12):
    for j in range (1,3):
        dvdt_all_plot(al1 = 'na12_orig1', al2= 'R850P', stim_amp=i*0.05,  stim_dur = j* 500 )
"""


#dvdt_all_plot(al1 = 'na12_orig1', al2= 'na12_R850P_old', stim_amp=0.7,  stim_dur = 500 )
#dvdt_all_plot(al1 = 'na12_orig1', al2= 'na12_R850P_5may', stim_amp=0.7,  stim_dur = 500 )
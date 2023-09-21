from NeuronModelClass import NeuronModel
from NrnHelper import *
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import numpy as np
class Na12ModelGY:
    def __init__(self,na12name = 'na12_orig1',mut_name= 'na12_R850P',  na12mechs = ['na12','na12mut'],na16name = 'na16_orig2', na16mechs = ['na16','na16mut'], params_folder = './params/',nav12=1,nav16=1,K=1,KT=1,KP=1,somaK=1,ais_ca = 1,ais_Kca = 1,soma_na16=1,soma_na12 = 1,node_na = 1,plots_folder = f'./Plots/'):
        ais_Kca = 0.5
        #K = 0.6
        #update_param_value(self.l5mdl,['SKv3_1'],'vtau',25)
        #ais_ca = 2
        #soma_na16 = 0.7
        #soma_na12 = 0.7
        #nav12 = 3
        #nav16 = 1
        #KP = 0.1
        #somaK = 2
        #KP=3
        #K=3
        #KT = 0.5
        nav12 = 1.2
        nav16 = 1.2
        
        #______________M1TTPC2
        nav12 = 3.5
        nav16 = 1.2
        ais_Kca = 0.03*ais_Kca
        ais_ca = 0.04*ais_ca
        KP=1.1*KP
        K = 4.8*K
        KT = 0.025*0.5*KT
        
       #______________GY
       # KP= KP
        
    

        self.l5mdl = NeuronModel(nav12=nav12, nav16=nav16,axon_K = K,axon_Kp = KP,axon_Kt = KT,soma_K = somaK,ais_ca = ais_ca,ais_KCa=ais_Kca,soma_nav16=soma_na16,soma_nav12 = soma_na12,node_na = node_na)
        update_param_value(self.l5mdl,['SKv3_1'],'mtaumul',6)
   
        self.mut_mech = [na12mechs[1]]  #new from Namut: different parameters for the wt and mut mechanisms
        self.wt_mech = [na12mechs[0]]   #new from Namut
        self.na16mechs = na16mechs
        self.plot_folder = plots_folder 
        #self.plot_folder = f'{plots_folder}/GY_R850P/'
        self.plot_folder = f'{plots_folder}/TIMTEST/' #########################*****************$*$*$*$
        Path(self.plot_folder).mkdir(parents=True, exist_ok=True)

     #this model originally makes het but if you put wt name as mut name it creates the WT and if you put mut name as
     #na12 name and mut_name then you will have homozygus
        self.l5mdl.h.working()                                                  
        p_fn_na12 = f'{params_folder}{na12name}.txt'  
        p_fn_na12_mech = f'{params_folder}{mut_name}.txt'
        print(f'using wt_file {na12name}')
        self.na12_p = update_mech_from_dict(self.l5mdl, p_fn_na12, self.wt_mech) 
        print(f'using mut_file {mut_name}')
        self.na12_pmech = update_mech_from_dict(self.l5mdl, p_fn_na12_mech, self.mut_mech)
        """
        print(f'using na16_file {na16name}')
        p_fn_na16 = f'{params_folder}{na16name}.txt'
        self.na16_p = update_mech_from_dict(self.l5mdl, p_fn_na16, self.na16mechs) 
        """

    def make_current_scape(self, sim_config = {
                        'section' : 'soma',
                        'segment' : 0.5,
                        'section_num': 0,
                        'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'],
                        'ionic_concentrations' :["cai", "ki", "nai"]
                        
                    }):

        self.l5mdl.init_stim(amp=0.5,sweep_len = 500)
        Vm, I, t, stim, ionic = self.l5mdl.run_sim_model(dt=0.01,sim_config=sim_config)
        return Vm, I, t, stim, ionic
        
        
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
        
            
    def plot_currents(self,stim_amp = 0.5,dt = 0.01,clr = 'black',plot_fn = 'step',axs = None, stim_dur = 500):
        if not axs:
            fig,axs = plt.subplots(4,figsize=(cm_to_in(8),cm_to_in(30)))
        self.l5mdl.init_stim(stim_dur = stim_dur, amp=stim_amp,sweep_len = 200)
        Vm, I, t, stim = self.l5mdl.run_model(dt=dt)
        axs[0].plot(t,Vm, label='Vm', color=clr,linewidth=1)
        axs[0].locator_params(axis='x', nbins=5)
        axs[0].locator_params(axis='y', nbins=8)
        
        axs[1].plot(t,I['Na'],label = 'Na',color = 'red')
        axs[2].plot(t,I['K'],label = 'K',color = 'black')
        axs[3].plot(t,I['Ca'],label = 'Ca',color = 'green')
        #add_scalebar(axs)
        file_path_to_save=f'{self.plot_folder}/Ktrials2_{plot_fn}.pdf'
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
        file_path_to_save=plot_fn
        plt.savefig(file_path_to_save, format='pdf', dpi=my_dpi)
        return axs
        
    def plot_fi_curve(self,start,end,nruns,wt_data = None,ax1 = None, fig = None,fn = 'ficurve'):
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

        
def scan_sec_na():
    for fac in np.arange(0.1,1,0.1):
        sim = Na12ModelGY(soma_na16=fac,soma_na12=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Na16_{fac}_Na12_{fac}.pdf'
        fig_volts.savefig(fn)
        """
        sim = Na12ModelGY(soma_na12=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Na12_{fac}.pdf'
        fig_volts.savefig(fn)

        sim = Na12ModelGY(node_na=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/node_na_{fac}.pdf'
        fig_volts.savefig(fn)
        """
def scan12_16():
    for i12 in np.arange(2,0.4,-0.5):
        for i16 in np.arange(2,0.4,-0.5):
            sim = Na12ModelGY(nav12=i12, nav16=i16)
            #sim.make_wt()
            fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
            sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
            plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
            fn = f'{sim.plot_folder}/vs_dvdt12_{i12}_16_{i16}.pdf'
            fig_volts.savefig(fn)

def scanK():
    for i in np.arange(0.1,5,0.5):

        

        sim = Na12ModelGY(ais_ca=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(10),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/ais_CA_{i}_.pdf'
        fig_volts.savefig(fn)
        
        sim = Na12ModelGY(ais_Kca=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(10),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/ais_Kca_{i}_.pdf'
        fig_volts.savefig(fn)
       
        sim = Na12ModelGY(K=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/K_{i}_.pdf'
        fig_volts.savefig(fn)
        
        sim = Na12ModelGY(somaK=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/somaK_{i}_.pdf'
        fig_volts.savefig(fn)


        sim = Na12ModelGY(KP=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Kp_{i}_.pdf'
        fig_volts.savefig(fn)



        sim = Na12ModelGY(KT=i)
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
        sim = Na12ModelGY()
        update_param_value(sim.l5mdl,['SKv3_1'],'vtau',vtau_orig+i)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/kv31_shift_vtau_{i}_.pdf'
        fig_volts.savefig(fn)
        update_param_value(sim.l5mdl,['SKv3_1'],'vtau',vtau_orig)

        
        sim = Na12ModelGY()
        update_param_value(sim.l5mdl,['SKv3_1'],'vinf',vinf_orig+i)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/kv31_shift_vinf_{i}_.pdf'
        fig_volts.savefig(fn)
        update_param_value(sim.l5mdl,['SKv3_1'],'vinf',vinf_orig)
    mtaumul_orig = 4
    for i in np.arange(0.1,1,0.2):
        sim = Na12ModelGY()
        update_param_value(sim.l5mdl,['SKv3_1'],'mtaumul',mtaumul_orig +i)
        fn = f'{sim.plot_folder}/kv31_shift_mtaumul_{i}_.pdf'
        sim.plot_axonal_ks(plot_fn = fn)
    update_param_value(sim.l5mdl,['SKv3_1'],'mtaumul',mtaumul_orig)
        

def scanKT():
    vshift_orig = -10
    for i in np.arange(10,31,10):
        sim = Na12ModelGY()
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
        sim = Na12ModelGY(na16name = na16_name)
        sim.plot_currents()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.5,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/default_na16_{i}.pdf'
        fig_volts.savefig(fn)

def default_model(al1 = 'na12_orig1', al2= 'na12_orig1', typ= ''):
    sim = Na12ModelGY(al1,al2)
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
    sim = Na12ModelGY(al1,al2)
    
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
    fn = f'./Plots/GY_R850P/{al2}_{stim_amp}_{stim_dur}.pdf'
    fig_volts.savefig(fn)




#sim = Na12ModelGY('na12_orig1', 'na12_orig1')
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
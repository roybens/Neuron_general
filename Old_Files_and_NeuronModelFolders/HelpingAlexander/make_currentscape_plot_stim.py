def make_currentscape_plot_stim(self,stim, dt, start_Vm=-72, sim_config = {
                    'section' : 'soma',
                    'segment' : 0.5, ##0.5 should be half way down AIS
                    'section_num': 0,
                    'currents'  :  ['cm','gCa_HVAbar_Ca_HVA','gSKv3_1bar_SKv3_1','gSK_E2bar_SK_E2','gCa_LVAstbar_Ca_LVAst','gIhbar_Ih','gamma_CaDynamics_E2','gbar_na12','gbar_na12mut','gbar_na16', 'gbar_na16mut', 'g_pas'],
        # ['ihcn_Ih','ica_Ca_HVA','ica_Ca_LVAst','ik_SKv3_1','ik_SK_E2','na16.ina_ina','na16mut.ina_ina','na12.ina_ina','na12mut.ina_ina','i_pas'], ##Currents must be present in .mod files
                    #'currents'  :['ina','ica','ik'], ##Example if you have fewer currents
                    'ionic_concentrations' :["cai", "ki", "nai"]
            }):
            
            current_names = sim_config['currents'] ##Current names in order of 'currents'in sim_config. Or if you don't want different curent names, use- current_names = sim_config['currents']


            #amp = 0.5 ##Modify stimulus current
            #sweep_len = 800 ##Modify this to change total length of recording
            # self.init_stim(stim_start =stim_start,amp=amp,sweep_len = sweep_len) ##Modify stim_start to change with the stimulus starts. Helpful when looking at single APs
            Vm, I, t, stim, ionic = self.run_model_compare_cs(stim, dt=dt, start_Vm=start_Vm)
            
            Vm = np.array(Vm)
            

            ##### Below for plotting user-specified time steps
            # time1 = 51 ##start time. Must be between 0 < x < sweep_len
            # time2 = 60 ##end time. Must be between 0 < x < sweep_len
            time1  = 100
            time2  = len(stim) - 100
            step1 = int((time1/dt))
            step2 = int((time2/dt))
            Vmsteplist = Vm[step1:step2] ##assign new list for range selected between two steps
            maxvm = max(Vm[step1:step2]) ##gets max voltage
            indexmax = Vmsteplist.argmax() ##gets index (time point in Vmsteplist) where max voltage is
            #####
            self.plot_folder = 'plots'
            self.pfx = 'pfx'


            plot_config = {
                "output": {
                    "savefig": True,
                    #"dir": "./Plots/12HMM16HH_TF/SynthMuts_120523/Currentscape/", ##can hardcode output directory path
                    "dir": f"{self.plot_folder}",
                    #"fname": "Na12_mut22_1nA_800ms", ##Change file name here
                    "fname":f"{self.pfx}_34_{len(stim)}",
                    "extension": "pdf", ##choose pdf or other image extension
                    #"extension": "jpg",
                    "dpi": 600,
                    "transparent": False},

                "show":{#"total_contribution":True, ##adds pie charts for overall contribution of currents over full recording
                        #"all_currents":True, ##adds line plots below currents to to show currents over time (rather than just percentage of total)
                        "currentscape": True}, ##Shows currentscape

                "colormap": {"name":"colorbrewer.qualitative.Paired_10"}, ##Can change color pallets. The _# means how many colors in that pallette. If you don't have enough colors for each current to have unique color, some currents will not be displayed
                #"colormap": {"name":"cartocolors.qualitative.Prism_10"},
                #"colormap": {"name":"cmocean.diverging.Balance_10"},

                "xaxis":{"xticks":[25,50,75],
                         "gridline_width":0.2,},

                "current": {"names": current_names,
                            "reorder":False,
                            # "autoscale_ticks_and_ylim":False,
                            # "ticks":[0.00001, 0.001, 0.1], 
                            # "ylim":[0.00001,0.01] #yaxis lims[min,max]
                            },

                "ions":{"names": ["ca", "k", "na"], ##Ionic currents to be displayed at bottom of plot
                        "reorder": False},

                "voltage": {"ylim": [-90, 50]},
                "legendtextsize": 5,
                "adjust": {
                    "left": 0.15,
                    "right": 0.8,
                    "top": 1.0,
                    "bottom": 0.0
                    }
                }


            print(f"The max voltage value is {maxvm}")        
            print(f"The index at which the max voltage happens is {indexmax}")

            #fig = plot_currentscape(Vm, [I[x] for x in I.keys()], plot_config,[ionic[x] for x in ionic.keys()]) ##Default version that plots full sweep_len (full simulation)
            fig = currentscape.plot(Vm[step1:step2], [I[x][step1:step2] for x in I.keys()], plot_config,[ionic[x][step1:step2] for x in ionic.keys()]) ##Use this version to add time steps, must include time1 and time2 above
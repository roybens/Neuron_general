    def run_model_compare_cs(self, stim, dt, start_Vm=-72, sim_config = {
                'section' : 'soma',
                'section_num' : 0,
                'segment' : 0.5,
                'currents'  :['ina','ica','ik'],
                'ionic_concentrations' :["cai", "ki", "nai"]
            }):
        # updates the stimulation params used by the model
        # time values are in ms
        # amp values are in nA
        # clamp = h.st
        h.dt = dt
        h.finitialize(start_Vm)
        clamp = h.IClamp(h.cell.soma[0](0.5))
        clamp.delay = 0
        clamp.dur = 1e9
        timesteps = len(stim)
        v = []
        t = []
        current_types = sim_config['currents']
        ionic_types = sim_config['ionic_concentrations']
        
        I = {current_type: np.zeros(timesteps, dtype=np.float64) for current_type in current_types}
        
        ionic = {ionic_type : np.zeros(timesteps,dtype=np.float64) for ionic_type in ionic_types}
        
        section = sim_config['section']
        section_number = sim_config['section_num']
        segment = sim_config['segment']
        
        volt_var  = "h.cell.{section}[{section_number}]({segment}).v".format(section=section, section_number=section_number,segment=segment)
        curr_vars={}
        curr_vars = {current_type : "h.cell.{section}[{section_number}]({segment}).{current_type}".format(section=section, section_number=section_number, segment=segment, current_type=current_type) for current_type in current_types}
        print(f"current_vars : {curr_vars}")
        ionic_vars = {ionic_type : "h.cell.{section}[{section_number}]({segment}).{ionic_type}".format(section=section , section_number=section_number, segment=segment, ionic_type=ionic_type) for ionic_type in ionic_types}
        
        
        for timestep in range(len(stim)):
            h.dt = dt
            clamp.amp = stim[timestep]
            h.fadvance()
            v.append(h.cell.soma[0].v)
            t.append(dt)
            
            for current_type in current_types:
                I[current_type][timestep] = eval(curr_vars[current_type])

            for ionic_type in ionic_types:
                ionic[ionic_type][timestep] = eval(ionic_vars[ionic_type])
            # print(h.cell.soma[0].v, timestep)
            
        return v, I, t, stim, ionic
        
import datetime
import os

def save2text(weights=None, best_hof=None, init_WT=None, mutant_data=None, channel_name=None,
                          csv_file=None, mutant=None, cp_file=None, wild_type_params=None,
                          objective_names=None,
                          ais_nav12_fac=None,
                          ais_nav16_fac=None,
                          nav12=None,
                          nav16=None,
                          nav12name=None,
                          mutname=None,
                          nav16name=None,
                          ):
    # Create the directory if it doesn't exist
    directory = "Documentation"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the text file name with the current date and the value of the mutant variable
    current_date = datetime.date.today().strftime("%d_%m_%Y")
    text_file_name = f"{current_date}_{mutant}.txt"
    text_file_path = os.path.join(directory, text_file_name)

    # Write the variable documentation to the text file
    with open(text_file_path, "w") as text_file:
        text_file.write("Variable Documentation\n\n")
        text_file.write(f"weights: {weights}\n") if weights is not None else None
        text_file.write(f"best_hof: {best_hof}\n") if best_hof is not None else None
        text_file.write(f"init_WT: {init_WT}\n") if init_WT is not None else None
        text_file.write(f"mutant_data: {mutant_data}\n") if mutant_data is not None else None
        text_file.write(f"channel_name: {channel_name}\n") if channel_name is not None else None
        text_file.write(f"csv_file: {csv_file}\n") if csv_file is not None else None
        text_file.write(f"mutant: {mutant}\n") if mutant is not None else None
        text_file.write(f"cp_file: {cp_file}\n") if cp_file is not None else None
        text_file.write(f"wild_type_params: {wild_type_params}\n") if wild_type_params is not None else None
        text_file.write(f"objective_names: {objective_names}\n") if objective_names is not None else None
        
        ##Vars in NeuronGeneral
        text_file.write(f"ais_nav12_fac: {ais_nav12_fac}\n") if ais_nav12_fac is not None else None
        text_file.write(f"ais_nav16_fac: {ais_nav16_fac}\n") if ais_nav16_fac is not None else None
        text_file.write(f"nav12: {nav12}\n") if nav12 is not None else None
        text_file.write(f"nav16: {nav16}\n") if nav16 is not None else None
        text_file.write(f"nav12name: {nav12name}\n") if nav12name is not None else None
        text_file.write(f"mutname: {mutname}\n") if mutname is not None else None
        text_file.write(f"nav16name: {nav16name}\n") if nav16name is not None else None
        

#save2text(weights, best_hof, evaluator.init_WT, evaluator.mutant_data, channel_name,csv_file, mutant, cp_file, wild_type_params,objective_names)

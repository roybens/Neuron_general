import os
import json
from pypdf import PdfMerger



def combine_pdfs(folder_path, out_sfx): #input folder pather where pdfs are stored, out_sfx = output suffix
    #folder_path = '/global/homes/t/tfenton/IC_Fitter/Plots_Folder/Tim_Plots/Na16/Na16_MORAN/'
    #merger = PdfMerger()
    merger = PdfMerger()
    #mutant = 'mut'+str(i)+'_'+str(j)
    #path = os.path.join(folder_path, mutant)
    os.chdir(folder_path)

    pdfs = ['HMM_Mutant_Inact.pdf','HMM_Mutant.pdf',
            'Ramp_Plots.pdf','RFI_Plots.pdf' ]
    
    for pdf in pdfs:
        merger.append(pdf)
    
    #merger.write(folder_path+"_combined100323.pdf")
    merger.write(folder_path+out_sfx+'.pdf')
    merger.close()
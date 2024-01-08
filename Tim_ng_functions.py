import itertools
import os
import json
from PyPDF2 import PdfMerger #need to write for pypdf
from pypdf import PdfWriter
from pypdf import PdfReader
import pandas as pd
import csv
import re
from pptx import Presentation
from pptx.util import Inches,Pt
from PIL import Image
import io
import fitz
import sys
import numpy as np

def combine_pdfs(folder_path, out_sfx): #input folder pather where pdfs are stored, out_sfx = output suffix
    file = open('/global/homes/t/tfenton/Neuron_general-2/JUPYTERmutant_list.txt','r') #put mutant names in here
    Lines = file.readlines() #read each mut name
    #os.chdir(folder_path)
    for line in Lines:
        mutTXT = line.strip() #remove return after each mut name
        print(mutTXT)
        mutfolderpath = os.path.join(folder_path,mutTXT)
        
        os.chdir(mutfolderpath)
        #
        #if filename.endswith(".pdf"):
            #merger.append(os.path.join(mutfolderpath, filename))
        merger = PdfMerger()
        #merger = PdfWriter() #for use with pypdf library *UNTESTED*

        # pdfs = [f'{mutTXT}__0.5_75.pdf',f'{mutTXT}__0.5_100.pdf',
        #         'test__fi.pdf','test_0.5_wtvmut.pdf','test_1_wtvmut.pdf']
        pdfs = ['test_0.5_wtvmut.pdf','test_1_wtvmut.pdf']
        
        for pdf in pdfs:
            merger.append(pdf)
        
        #merger.write(folder_path+"_combined100323.pdf")
        merger.write(folder_path+mutTXT+out_sfx+'.pdf')
    merger.close()

# def convert_pdf_to_jpg(pdf_path, output_jpg_path):
#     """
#     Converts a single page of a PDF to a JPG image.

#     Args:
#         pdf_path: Path to the PDF file.
#         output_jpg_path: Path to the output JPG image.
#     """

#     # Open the PDF and get the first page
#     reader = PdfReader(pdf_path)
#     page = reader.getPage(0)

#     # Extract the page content as a PIL Image object
#     pil_image = Image.open(page.extractImage()[0])

#     # Convert the image to RGB mode (required for JPG)
#     pil_image = pil_image.convert("RGB")

#     # Save the image as a JPG
#     pil_image.save(output_jpg_path, quality=95)

#     # Example usage
#     pdf_path = "/path/to/your.pdf"
#     output_jpg_path = "/path/to/output.jpg"
# convert_pdf_to_jpg(pdf_path, output_jpg_path)

# print(f"Successfully converted PDF page to JPG: {output_jpg_path}")


def combine_and_sort_ef_csvs(root_path, out_sfx):
  combined_ef = f'{root_path}combined_ef_{out_sfx}.csv'
  # Open the output file in write mode
  with open(combined_ef, "w", newline="") as outfile:
    writer = csv.writer(outfile)

    data_by_filename = {}

    # Loop through all folders in the current directory
    for folder in os.listdir(root_path):
      # Check if it's a directory and not a file
      if os.path.isdir(os.path.join(root_path, folder)):
        # Access files within the folder using another loop
        for filename in os.listdir(os.path.join(root_path, folder)):
          if filename.endswith(".csv"):
            # Extract mutation number and index from filename
            match = re.search(r"mut(\d+)_(\d+)_", filename)
            if match:
              mutation_number, index = match.groups()

              # Open and process the CSV file
              with open(os.path.join(root_path, folder, filename), "r", newline="") as infile:
                reader = csv.reader(infile)

                # Skip the header
                next(reader)

                # Store data row with filename information as key
                for row in reader:
                  data_by_filename[f"{mutation_number}_{index}_{filename}"] = row

    # Sort data based on filename key (automatically sorts based on structure)
    sorted_data = sorted(data_by_filename.items(), key=lambda item: item[0])

    # Write sorted data to the output file
    for key, row in sorted_data:
      writer.writerow(row)

  print(f"Successfully combined and sorted data into '{combined_ef}'!")
  return




#####NOT WORKING!!!!!!!!!!!!!!!!!!!!!!!!
# def make_ppt_from_pdf(pdf_path, output_ppt_path):
#     # Define paths and presentation object
    
#     prs = Presentation()
#     blank_slide_layout = prs.slide_layouts[6]
#     slide = prs.slides.add_slide(blank_slide_layout)
#     left = top = width = height = Inches(0.5)
#     top = 0.2
#     width = 6
#     height=2
    
#     file = open("/global/homes/t/tfenton/Neuron_general-2/JUPYTERmutant_list.txt", "r")
#     lines = file.readlines()

    

#     for line in lines: #mut1_1,mut1_2 etc.
#         mut_txt = line.strip()
#         print(mut_txt)

#         for filename in os.listdir(f"{pdf_path}{mut_txt}"): #files within each mut folder
#             if filename.endswith(".pdf"):
#                 reader = PdfReader(os.path.join(f"{pdf_path}{mut_txt}", filename))
#                 print(os.path.join(f"{pdf_path}/{mut_txt}", filename))
#                 file = os.path.join(f"{pdf_path}/{mut_txt}", filename)

#                 pdf_file = fitz.open(file)
#                 for page_index in range(len(pdf_file)):
#                    page = pdf_file[page_index]
#                    image_list = page.getImageList()
#                    if image_list:
#                         print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
#                    else:
#                         print("[!] No images found on page", page_index) 
                      
#                    for image_index, img in enumerate(page.getImageList(), start=1): 
#                         slide = prs.slides.add_slide(blank_slide_layout)
#                         txBox = slide.shapes.add_textbox(left,top,width,height)
#                         tf = txBox.text_frame
#                         tf.text = mut_txt
#                         # get the XREF of the image 
#                         xref = img[0] 
                  
#                         # extract the image bytes 
#                         base_image = pdf_file.extractImage(xref) 
#                         image_bytes = base_image["image"] 
                  
#                         # get the image extension 
#                         image_ext = base_image["ext"] 
#                         pil_image = Image.open(io.BytesIO(base_image))
#                         pil_image = pil_image.convert("RGB")
#                         # image_path = os.path.join(image_folder, f"{mut_txt}_{count}.jpg")
#                         # pil_image.save(image_path)
#                         # count += 1
#                         # Add the saved image to the slide
#                         slide.shapes.add_picture(pil_image)
 

#     prs.save(output_ppt_path)
#     print(f"Successfully converted PDFs to PowerPoint presentation: {output_ppt_path}")



def make_ppt_from_pdf2(pdf_path, output_ppt_path):
  prs = Presentation()
  blank_slide_layout = prs.slide_layouts[6]
  slide = prs.slides.add_slide(blank_slide_layout)
  left = top = width = height = Inches(0.5)
  
  
  # file = open("/global/homes/t/tfenton/Neuron_general-2/JUPYTERmutant_list.txt", "r")
  # lines = file.readlines()
  # for line in lines: #mut1_1,mut1_2 etc.
  #   mut_txt = line.strip()
  #   print(mut_txt)
    
  for folder in sorted(os.listdir(pdf_path)): #Sort the listed directories so output pptx is somewhat in order 
      if os.path.isdir(os.path.join(pdf_path, folder)):# Check if it's a directory
        slide = prs.slides.add_slide(blank_slide_layout) #Add slide for each folder. Each slide will have multiple plots on it
        txBox = slide.shapes.add_textbox(left,top,width,height) #Add text box for title
        tf = txBox.text_frame
        page_count = 0
        for filename in sorted(os.listdir(os.path.join(pdf_path, folder))):# Access files within the folder, and sort them to appear in sam order on slide
          if filename.endswith(".pdf"):
  
            file = os.path.join(pdf_path,folder, filename) #pdf file path
            
            tf.text = folder
            print(folder)
            
            doc = fitz.open(file)
            for page in doc:  # iterate through the pages
              pix = page.get_pixmap(dpi=150)  # render page to an image
              pix.save(f"{pdf_path}/{folder}-{filename}.png")  # store image as a PNG
              
              
              slide.shapes.add_picture(f"{pdf_path}/{folder}-{filename}.png",left=Inches(page_count*2.5),top=Inches(1), width=Inches(2.5))
              print(page_count)
          page_count+=1
          
  
  prs.save(output_ppt_path)
  print(f"Successfully converted PDFs to PowerPoint presentation: {output_ppt_path}")
  return





#combine_pdfs(folder_path='/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/AllSynthMuts_121223/', out_sfx='traceDVDTfi_121323')


#combine_and_sort_ef_csvs(root_path='/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/AllSynthMuts_121223/', out_sfx='allsynthmuts_121323_sorted')

make_ppt_from_pdf2(pdf_path='/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/SynthMuts_scanNa12_121523',
                  output_ppt_path='/global/homes/t/tfenton/Neuron_general-2/Plots/12HMM16HH_TF/SynthMuts_scanNa12_121523/ScanNa12_synthmuts_010224.pptx')






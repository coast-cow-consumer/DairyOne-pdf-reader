# process_pdf.py

import os
import shutil
from g_drive_service import GDriveService
from analysis_data_extract import extract_analysis_data_and_to_csv
from tfa_data_extract import extract_tfa_data_and_to_csv
from fermentation_data_extract import extract_fermentation_data_and_to_csv
from macros_data_extract import extract_macro_data_and_to_csv



if __name__ == "__main__":
    serv = GDriveService()
    serv.List_All_Drive_Files()
   
    #ANALYSIS

    # get a list of the current files in the pdf drop folder
    analysis_items = serv.List_PDF_Folder("analysis")
    files_analysis_pdf_folder = []
    print("Downloaded Analysis Files:")
    for f in analysis_items:
        print("\t",f["name"], f["id"], f.get("parents"))
        files_analysis_pdf_folder.append( (f["id"], f["name"],) ) # append tuple with name and id

    # create a folder on the vm to store the downloaded files
    analysis_pdf_download_path = "analysis_target/"
    if not os.path.exists(analysis_pdf_download_path):
        os.makedirs(analysis_pdf_download_path)

    # download files to that folder
    for f in files_analysis_pdf_folder:
        location = analysis_pdf_download_path+f[1]
        serv.download(f[0],location)

    # create folder to place csv
    analysis_csv_path = "analysis_csv/"
    if not os.path.exists(analysis_csv_path):
        os.makedirs(analysis_csv_path)

    # process the files into folder created above
    for f in files_analysis_pdf_folder:
        extract_analysis_data_and_to_csv(analysis_pdf_download_path+f[1], analysis_csv_path)

    # loop through files in analysis folder, and upload those to drive
    for f in os.listdir(analysis_csv_path):
        if os.path.isfile(os.path.join(analysis_csv_path, f)) and not f.startswith('.'):
                f_path = os.path.join(analysis_csv_path, f)
                if f_path.endswith("_m.csv"):
                    dest = serv.manure_folder_id
                elif f_path.endswith("_o.csv"):
                    dest = serv.other_folder_id
                elif f_path.endswith("_d.csv"):
                    dest = serv.dryae_folder_id
                elif f_path.endswith("_t.csv"):
                    dest = serv.tmr_folder_id
                elif f_path.endswith("_g.csv"):
                    dest = serv.grain_folder_id
                else:
                    dest = serv.unrecognized_folder_id
                serv.upload(f_path, f, dest, "CSV")
    #clear csv directory
    shutil.rmtree(analysis_csv_path)     
    # once everything has happened, move pdfs in drive to used folder
    for f in files_analysis_pdf_folder:
        serv.Move_File(f[0], serv.used_PDF_folder_id)



    ##TFA


    tfa_items = serv.List_PDF_Folder("tfa")
    files_tfa_pdf_folder = []
    print("Downloaded TFA Files:")
    for f in tfa_items:
        print("\t",f["name"], f["id"], f.get("parents"))
        files_tfa_pdf_folder.append( (f["id"], f["name"],) ) # append tuple with name and id

    # create a folder on the vm to store the downloaded files
    tfa_pdf_download_path = "tfa_target/"
    if not os.path.exists(tfa_pdf_download_path):
        os.makedirs(tfa_pdf_download_path)

    # download files to that folder
    for f in files_tfa_pdf_folder:
        location = tfa_pdf_download_path+f[1]
        serv.download(f[0],location)

    # create folder to place csv in on vm
    tfa_csv_path = 'acid_csv/'
    if not os.path.exists(tfa_csv_path):
        os.makedirs(tfa_csv_path)

    # process the files into folder created above
    for f in files_tfa_pdf_folder:
        extract_tfa_data_and_to_csv(tfa_pdf_download_path+f[1], tfa_csv_path)

    # loop through files in analysis folder, and upload those to drive
    for f in os.listdir(tfa_csv_path):
        if os.path.isfile(os.path.join(tfa_csv_path, f)) and not f.startswith('.'):
                f_path = os.path.join(tfa_csv_path, f)
                serv.upload(f_path, f, serv.tfa_folder_id, "CSV")
    shutil.rmtree(tfa_csv_path) 
    # once everything has happened, move pdfs in drive to used folder
    for f in files_tfa_pdf_folder:
        serv.Move_File(f[0], serv.used_PDF_folder_id)
    

    #FERMENT

    ferment_items = serv.List_PDF_Folder("ferment")
    files_ferment_pdf_folder = []
    print("Downloaded Fermentation Files:")
    for f in ferment_items:
        print("\t",f["name"], f["id"], f.get("parents"))
        files_ferment_pdf_folder.append( (f["id"], f["name"],) ) # append tuple with name and id

    # create a folder on the vm to store the downloaded files
    ferment_pdf_download_path = "ferment_target/"
    if not os.path.exists(ferment_pdf_download_path):
        os.makedirs(ferment_pdf_download_path)

    # download files to that folder
    for f in files_ferment_pdf_folder:
        location = ferment_pdf_download_path+f[1]
        serv.download(f[0],location)

    # create folder to place csv in on vm
    ferment_path = 'ferm_csv/'
    if not os.path.exists(ferment_path):
        os.makedirs(ferment_path)

    # process the files into folder created above
    for f in files_ferment_pdf_folder:
        extract_fermentation_data_and_to_csv(ferment_pdf_download_path+f[1], ferment_path)

    # loop through files in analysis folder, and upload those to drive
    for f in os.listdir(ferment_path):
        if os.path.isfile(os.path.join(ferment_path, f)) and not f.startswith('.'):
                f_path = os.path.join(ferment_path, f)
                serv.upload(f_path, f, serv.ferment_folder_id, "CSV")
    shutil.rmtree(ferment_path)  

    #MACRO

    
    macro_items = serv.List_PDF_Folder("macro")
    files_macro_pdf_folder = []
    print("Downloaded Macro Files:")
    for f in macro_items:
        print("\t",f["name"], f["id"], f.get("parents"))
        files_macro_pdf_folder.append( (f["id"], f["name"],) ) # append tuple with name and id

    # create a folder on the vm to store the downloaded files
    macro_pdf_download_path = "macro_target/"
    if not os.path.exists(macro_pdf_download_path):
        os.makedirs(macro_pdf_download_path)

    # download files to that folder
    for f in files_macro_pdf_folder:
        location = macro_pdf_download_path+f[1]
        serv.download(f[0],location)

    # create folder to place csv in on vm
    macro_csv_path = 'macro_csv/'
    if not os.path.exists(macro_csv_path):
        os.makedirs(macro_csv_path)

    # process the files into folder created above
    for f in files_macro_pdf_folder:
        extract_macro_data_and_to_csv(macro_pdf_download_path+f[1], macro_csv_path)

    # loop through files in analysis folder, and upload those to drive
    for f in os.listdir(macro_csv_path):
        if os.path.isfile(os.path.join(macro_csv_path, f)) and not f.startswith('.'):
            f_path = os.path.join(macro_csv_path, f)
            serv.upload(f_path, f, serv.macro_folder_id, "CSV")
    shutil.rmtree(macro_csv_path) 
    # once everything has happened, move pdfs in drive to used folder
    for f in files_macro_pdf_folder:
        serv.Move_File(f[0], serv.used_PDF_folder_id)

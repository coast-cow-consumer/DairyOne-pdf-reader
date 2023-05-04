# process_pdf.py

import os
from g_drive_service import GDriveService
from analysis_data_extract import extract_analysis_data_and_to_csv
from tfa_data_extract import extract_tfa_data_and_to_csv
from fermentation_data_extract import extract_fermentation_data_and_to_csv




if __name__ == "__main__":
    serv = GDriveService()

    #logs and other info can be found in github actions page of this repo

    #TODO: rename some variables so they are not reused, and dont cause problems

    # start with analysis

    # get a list of the current files in the pdf drop folder
    analysis_items = serv.List_PDF_Folder("analysis")
    files_in_pdf_folder = []
    print("Downloaded files:")
    for f in analysis_items:
        print("\t",f["name"], f["id"], f.get("parents"))
        files_in_pdf_folder.append( (f["id"], f["name"],) ) # append tuple with name and id

    # create a folder on the vm to store the downloaded files
    download_path = "analysis_target/"
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # download files to that folder
    for f in files_in_pdf_folder:
        location = download_path+f[1]
        serv.download(f[0],location)

    # create folder to place csv in on vm
    analysis_path = "Analysis_Data/"
    if not os.path.exists(analysis_path):
        os.makedirs(analysis_path)

    # process the files into folder created above
    for f in files_in_pdf_folder:
        extract_analysis_data_and_to_csv(download_path+f[1], analysis_path)

    # loop through files in analysis folder, and upload those to drive
    for f in os.listdir(analysis_path):
        if os.path.isfile(os.path.join(analysis_path, f)):
            if not f.startswith('.'):
                f_path = os.path.join(analysis_path, f)
                serv.upload(f_path, f, serv.analysis_folder_id, "CSV")

    # once everything has happened, move pdfs in drive to used folder
    for f in files_in_pdf_folder:
        serv.Move_File(f[0], serv.used_PDF_folder_id)



    tfa_items = serv.List_PDF_Folder("tfa")
    files_in_pdf_folder = []
    print("Downloaded files:")
    for f in tfa_items:
        print("\t",f["name"], f["id"], f.get("parents"))
        files_in_pdf_folder.append( (f["id"], f["name"],) ) # append tuple with name and id

    # create a folder on the vm to store the downloaded files
    download_path = "tfa_target/"
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # download files to that folder
    for f in files_in_pdf_folder:
        location = download_path+f[1]
        serv.download(f[0],location)

    # create folder to place csv in on vm
    tfa_path = 'TFA_Data/'
    if not os.path.exists(tfa_path):
        os.makedirs(tfa_path)

    # process the files into folder created above
    for f in files_in_pdf_folder:
        extract_analysis_data_and_to_csv(download_path+f[1], tfa_path)

    # loop through files in analysis folder, and upload those to drive
    for f in os.listdir(tfa_path):
        if os.path.isfile(os.path.join(tfa_path, f)):
            if not f.startswith('.'):
                f_path = os.path.join(tfa_path, f)
                serv.upload(f_path, f, serv.tfa_folder_id, "CSV")

    # once everything has happened, move pdfs in drive to used folder
    for f in files_in_pdf_folder:
        serv.Move_File(f[0], serv.used_PDF_folder_id)
    


    ferment_items = serv.List_PDF_Folder("ferment")
    files_in_pdf_folder = []
    print("Downloaded files:")
    for f in ferment_items:
        print("\t",f["name"], f["id"], f.get("parents"))
        files_in_pdf_folder.append( (f["id"], f["name"],) ) # append tuple with name and id

    # create a folder on the vm to store the downloaded files
    download_path = "ferment_target/"
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # download files to that folder
    for f in files_in_pdf_folder:
        location = download_path+f[1]
        serv.download(f[0],location)

    # create folder to place csv in on vm
    ferment_path = 'Fermentation_Data/'
    if not os.path.exists(ferment_path):
        os.makedirs(ferment_path)

    # process the files into folder created above
    for f in files_in_pdf_folder:
        extract_analysis_data_and_to_csv(download_path+f[1], ferment_path)

    # loop through files in analysis folder, and upload those to drive
    for f in os.listdir(ferment_path):
        if os.path.isfile(os.path.join(ferment_path, f)):
            if not f.startswith('.'):
                f_path = os.path.join(ferment_path, f)
                serv.upload(f_path, f, serv.ferment_folder_id, "CSV")

    # once everything has happened, move pdfs in drive to used folder
    for f in files_in_pdf_folder:
        serv.Move_File(f[0], serv.used_PDF_folder_id)
    
# process_pdf.py

import os
from g_drive_service import GDriveService
from analysis_data_extract import extract_analysis_data_and_to_csv
if __name__ == "__main__":
    serv = GDriveService()

    #logs and other info can be found in github actions page of this repo

    # get a list of the current files in the pdf drop folder
    items = serv.List_PDF_Folder()
    files_in_pdf_folder = []
    print("Downloaded files:")
    for f in items:
        print("\t",f["name"], f["id"], f.get("parents"))
        files_in_pdf_folder.append( (f["id"], f["name"],) ) # append tuple with name and id

    # create a folder on the vm to store the downloaded files
    download_path = "target/"
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
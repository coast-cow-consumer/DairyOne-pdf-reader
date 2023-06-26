import io
import os
import googleapiclient
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class GDriveService:
    '''
    Docs for this:
    https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index.html


    NOTE: if a method isnt working or has a 403 error, try adding 'supportsTeamDrives=True, includeTeamDriveItems=True, driveId=self.shared_drive_id,' to the parameters of the method
        on the docs, it says shared drive is deprecated, but you still have to add it in order for most things to work


    '''
    def __init__(self):
        self.scopes=['https://www.googleapis.com/auth/drive']
        self.shared_drive_id = "0ABU_pocBghzEUk9PVA"

        #where people should drop the pdfs
        self.ANALYSIS_folder_id = "1DDPpLVPx2IK6WKtS2uclE5l20VUItOYP"
        self.TFA_folder_id = "1HTCUDwi-fvUYISCHKEmWmzw2Pe8cXs43"
        self.MACRO_folder_id = "1uRxaoFcShtLgweFuIRLdEuTNqwolNiOE"

        self.PDF_folder_id = "1QJg2gqGf_QK48w51NwNucWXn9BLpiSYn"
        self.used_PDF_folder_id = "17rldCORuNDIxYsksGE2U6XtMVz9_O-6I"

        #destination for processed data
        self.tfa_folder_id = "1KmVmrCdHI9uW5fmoWGtXXtgiowjMVpT8"
        self.macro_folder_id = "1ZoRfBaTe-LWkEuXsZNQt1-Zampxcv2At"
        self.manure_folder_id = "1JnlBbLI5lUNbHFyMHhbDtmGjUT1bDwNj"
        self.other_folder_id = "1FPJEMnXTfbp8qddXX7JQlVPUGodkSMzn"
        self.dryae_folder_id = "1vYscfLouxhBFWkF425tGswKevHcGcBoy"
        self.tmr_folder_id = "18KvxHQQnGsOroCt7GmGQCn6LVM3Grx8"
        self.grain_folder_id = "1QLWhZC1Fux2_5ssrH08dZ-y0fQOmBEC8"
        self.unrecognized_folder_id = "1yVZe2sYGxuuXo6YPvsbkhGUN02KrbazL"
        #command line: export DRIVE_KEY = "path/to/keyfile.json"
        keyfile = '/Users/gordondoore/Desktop/testfolder/service_acc_key_1.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, self.scopes)
        service = build('drive', 'v3', credentials=creds)
        self.GD_serv = service
        self.help()

    def List_All_Drive_Files(self):
        '''
        List all the files in the shared drive specified above

        returns a list of dictionaries, each entry in the list is a file, and that entry is a dict of all the drive api info about that file
        '''
        s = self.GD_serv

        files_list = s.files().list(supportsTeamDrives=True, includeTeamDriveItems=True, corpora="drive", driveId=self.shared_drive_id, q="trashed = false").execute()
        return files_list.get("files")
    
    def Remove_All_Files(self, folder_id):
        '''
        Removes all files in the specified folder.
        '''
        files_list = self.List_Drive_Directory(folder_id)
        if files_list:
            for file in files_list:
                file_id = file['id']
                try:
                    self.GD_serv.files().delete(fileId=file_id).execute()
                    print(f"Deleted file: {file_id}")
                except googleapiclient.errors.HttpError as e:
                    print(f"Error deleting file: {file_id}")
                    print(f"File name: {file['name']}")
                    print(f"Error details: {e.content}")
        else:
            print("No files found in the folder.")

    
    def List_Drive_Directory(self, folder_id):
        '''
        List all the files and folders in the specified Google Drive directory.

        Returns a list of dictionaries, where each entry represents a file or folder,
        containing information about the item.
        '''
        query_string = f"'{folder_id}' in parents and trashed = false"
        drive_service = self.GD_serv
        files_list = drive_service.files().list(
            supportsTeamDrives=True,
            includeTeamDriveItems=True,
            corpora='drive',
            driveId=self.shared_drive_id,
            q=query_string
        ).execute()
        return files_list.get('files', [])
    

    def List_PDF_Folder(self, folder_name):
        '''
        list all the files in the folder located at self.PDF_folder_id

        returns a list of dictionaries, each entry in the list is a file, and that entry is a dict of all the drive api info about that file
        '''

        if folder_name.lower() == "analysis":
            pdf_folder = self.ANALYSIS_folder_id
        elif folder_name.lower() == "tfa":
            pdf_folder = self.TFA_folder_id
        elif folder_name.lower() == "macro":
            pdf_folder = self.MACRO_folder_id
        else:
            print("Error: no folder specified or incorrect name")
            return

        q_string = "'{}' in parents and trashed = false".format(pdf_folder)
        s = self.GD_serv
        files_list = s.files().list(supportsTeamDrives=True, includeTeamDriveItems=True, corpora="drive", driveId=self.shared_drive_id, q=q_string).execute()
        return files_list.get("files")
    

    def get_file_parents(self, file_id):
        '''
        Returns the parents of a particular file

        useful for finding folder structures etc, and getting parent id for moving files around
        '''
        file = self.GD_serv.files().get(fileId=file_id, supportsTeamDrives=True, supportsAllDrives=True).execute()
        return file.get('parents')


    def Move_File(self, file_id, target_folder_id):
        '''
        moves the file at (file_id) to the location of (target_folder_id)
        '''

        file = self.GD_serv.files().get(fileId=file_id, supportsTeamDrives=True, supportsAllDrives=True, fields='parents').execute()
        prev_parents = ",".join(file.get('parents'))

        file = self.GD_serv.files().update(
                supportsTeamDrives=True, 
                supportsAllDrives=True,
                fileId=file_id,
                addParents=target_folder_id,
                removeParents=prev_parents,
                fields='id, parents'
            ).execute()

        print("moved", file_id,"to", target_folder_id)
    
    def rename_file(self, file_id, new_title):
        '''
        Change the name of a file at file_id to the new_title
        '''
        file = self.GD_serv.files().get(fileId=file_id)
        file["name"] = new_title
        file = self.GD_serv.files().update(fileId=file_id, body=file, supportsTeamDrives=True, supportsAllDrives=True).execute()
        return file

    def download(self, file_id, download_path):
        req = self.GD_serv.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, req)
        done = False
        while done is False:
            _, done = downloader.next_chunk()
            print("Download complete")
        with io.open(download_path, "wb") as f:
            fh.seek(0)
            f.write(fh.read())
        return

    def upload(self, filepath, name, dest_id, filetype):
        '''
        Upload the file at a given filepath to the root of the shared drive in self.shared_drive_id
        '''

        if filetype == "PDF":
            mimetype = 'application/pdf'
        if filetype == "CSV":
            mimetype = 'text/csv'
        else:
            mimetype = '*/*'

        file = {
            'name': name,
            'mimeType': mimetype,
            'parents':[dest_id]
        }

        media = MediaFileUpload(filepath,
                                mimetype=mimetype)
    
        file = self.GD_serv.files().create(body=file, media_body=media, fields='id', supportsTeamDrives=True).execute()
        print('Upload success, File ID: ' + file.get('id'))
        return

    
    def help(self):
        '''
        print info about current drive service
        '''
        help_str =  "------------------------------------\n"
        help_str += "current drive id: " + self.shared_drive_id + "\n"
        help_str += "current PDF folder id: " + self.PDF_folder_id + "\n"
        help_str += "current Used_pdf folder id: " + self.used_PDF_folder_id + "\n"
        help_str += "current Macro folder id: " + self.macro_folder_id + "\n"
        help_str += "------------------------------------\n"
        print(help_str)

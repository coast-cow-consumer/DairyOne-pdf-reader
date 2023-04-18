import io
import os
from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class GDriveService:
    '''
    Docs for this:
    https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index.html
    '''
    def __init__(self):
        self.scopes=['https://www.googleapis.com/auth/drive']
        self.shared_drive_id = "0AB-fv-UfPPDzUk9PVA"

        self.PDF_folder_id = "1fSZbb7SXtV9hzfj3llku49abnLyoJVDf"
        self.used_PDF_folder_id = "1bMgv-f7Q9blI7vCaX7wrcmKrgxbhTCi6"
        self.analysis_folder_id = "1Q89MfH12q_RlsvqxG6Rzbf7dO-KbrvGy"

        keyfile = os.environ.get('LB_DRIVE_KEY')
        creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, self.scopes)
        service = build('drive', 'v3', credentials=creds)
        self.GD_serv = service

    def List_All_Drive_Files(self):
        '''
        List all the files in the shared drive specified above

        returns a list of dictionaries, each entry in the list is a file, and that entry is a dict of all the drive api info about that file
        '''
        s = self.GD_serv

        files_list = s.files().list(supportsTeamDrives=True, includeTeamDriveItems=True, corpora="drive", driveId=self.shared_drive_id, q="trashed = false").execute()
        return files_list.get("files")

    def List_PDF_Folder(self):
        '''
        list all the files in the folder located at self.PDF_folder_id

        returns a list of dictionaries, each entry in the list is a file, and that entry is a dict of all the drive api info about that file
        '''
        q_string = "'{}' in parents and trashed = false".format(self.PDF_folder_id)
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
        help_str += "current Analysis folder id: " + self.analysis_folder_id + "\n"
        help_str += "------------------------------------\n"
        print(help_str)

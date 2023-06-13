import io
import os
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

class GDriveService:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.PDF_folder_id = "1wVaiqvATuOS1pzmQ0KtUGHv7G9Sl_cIs"
        self.used_PDF_folder_id = "1Jhz5xeY9Uzkpu7fHpvesaGfGmZORzO6I"
        self.analysis_folder_id = "101CTwmHreVLhvhW1pGp7"
        self.tfa_folder_id = "1P4NAQFgkl2zsRYGTbgDDW1PSbXrHtYn5"
        self.ferment_folder_id = "1oDBtd0ynXqtrF9_9ccC4ZlUYZN3qdnkg"

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        service = build('drive', 'v3', credentials=creds)
        self.GD_serv = service
        self.help()

    def List_All_Drive_Files(self):
        s = self.GD_serv
        drive_files = []
        results = s.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            df = u'{0} ({1})'.format(item['name'], item['id'])
            drive_files.append(df)
            print(df)
        return drive_files

    def List_PDF_Folder(self, folder_name):
        if folder_name.lower() == "analysis":
            pdf_folder = self.analysis_folder_id
        elif folder_name.lower() == "tfa":
            pdf_folder = self.tfa_folder_id
        elif folder_name.lower() == "ferment":
            pdf_folder = self.ferment_folder_id
        else:
            print("Error: no folder specified or incorrect name")
            return
        q_string = "'{}' in parents and trashed = false".format(pdf_folder)
        s = self.GD_serv
        files_list = s.files().list(q=q_string).execute()
        return files_list.get("files")

    def get_file_parents(self, file_id):
        file = self.GD_serv.files().get(fileId=file_id).execute()
        return file.get('parents')

    def Move_File(self, file_id, target_folder_id):
        file = self.GD_serv.files().get(fileId=file_id, fields='parents').execute()
        prev_parents = ",".join(file.get('parents'))

        file = self.GD_serv.files().update(
            fileId=file_id,
            addParents=target_folder_id,
            removeParents=prev_parents,
            fields='id, parents'
        ).execute()

        print("moved", file_id, "to", target_folder_id)

    def rename_file(self, file_id, new_title):
        file = self.GD_serv.files().get(fileId=file_id).execute()
        file["name"] = new_title
        file = self.GD_serv.files().update(fileId=file_id, body=file).execute()
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
        if filetype == "PDF":
            mimetype = 'application/pdf'
        if filetype == "CSV":
            mimetype = 'text/csv'
        else:
                mimetype = '*/*'

        file = {
            'name': name,
            'mimeType': mimetype,
            'parents': [dest_id]
        }

        media = MediaFileUpload(filepath, mimetype=mimetype)

        file = self.GD_serv.files().create(
            body=file, media_body=media, fields='id'
        ).execute()
        print('Upload success, File ID: ' + file.get('id'))
        return

    def help(self):
        help_str = "------------------------------------\n"
        help_str += "current PDF folder id: " + self.PDF_folder_id + "\n"
        help_str += "current Used_pdf folder id: " + self.used_PDF_folder_id + "\n"
        help_str += "current Analysis folder id: " + self.analysis_folder_id + "\n"
        help_str += "------------------------------------\n"
        print(help_str)


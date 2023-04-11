import io
from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class GDriveService:
    # TODO: upload keys for C3 Drive to github, and test these more
    '''
    Docs for this:
    https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index.html
    '''
    def __init__(self):
        self.scopes=['https://www.googleapis.com/auth/drive']
        self.shared_drive_id = ""
        self.PDF_folder_id = ""

        creds = ServiceAccountCredentials.from_json_keyfile_name("eco-shift.json", self.scopes)
        service = build('drive', 'v3', credentials=creds)
        self.GD_serv = service

    def List_All_Drive_Files(self):
        '''
        List all the files in the shared drive specified above

        returns a list of dictionaries, each entry in the list is a file, and that entry is a dict of all the drive api info about that file
        '''
        s = self.GD_serv

        files_list = s.files().list(supportsTeamDrives=True, includeTeamDriveItems=True, corpora="drive", driveId=self.shared_drive_id).execute()
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

        !!! Not currently working, not sure why, use copy_move() instead

        moves the file at (file_id) to the location of (target_folder_id)

        '''
        prev_parents = self.get_file_parents(file_id)
        print(prev_parents)
        if prev_parents is not None:
            print("A")
            file = self.GD_serv.files().update(fileId=file_id,  supportsTeamDrives=True, supportsAllDrives=True, addParents=target_folder_id, removeParents=prev_parents, fields='id, parents').execute()
        else:
            print("HERE")
            file = self.GD_serv.files().update(fileId=file_id,  supportsTeamDrives=True, supportsAllDrives=True, addParents=target_folder_id, fields='id, parents').execute()

        if file.get('parents') != target_folder_id:
            print("error new file parents not added:")
            print("Target: ", target_folder_id)
            print("Actual: ", file.get('parents'))
            return False
        return True
    
    def rename_file(self, file_id, new_title):
        '''
        Change the name of a file at file_id to the new_title
        '''
        file = self.GD_serv.files().get(fileId=file_id)
        file["name"] = new_title
        file = self.GD_serv.files().update(fileId=file_id, body=file, supportsTeamDrives=True, supportsAllDrives=True).execute()
        return file

    def copy_move(self, file_id, target_folder_id):
        '''
        creates a copy of the original file, in a new location

        TODO: add a delete call to the original file
        '''
        newfile = {'DriveId':self.shared_drive_id, 'title': "lll_doc_version", 'parents' : [target_folder_id]}
        self.GD_serv.files().copy(fileId=file_id, body=newfile, supportsTeamDrives=True, supportsAllDrives=True).execute()

        print("copied file")

        self.rename_file(file_id, "MY NEW TITLE")
        return 

    def download(self, file_id, download_path):
        req = self.GD_serv.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, req)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(download_path, "wb") as f:
            fh.seek(0)
            f.write(fh.read())
        return

    def upload(self, filepath):
        '''
        Upload the file at a given filepath to the root of the shared drive in self.shared_drive_id

        TODO: add option to specify where the file goes within the drive
        TODO: add option to change mimetype so that different kinds of files can be uploaded with this function

        '''
        file = {
            'name': filepath,
            'mimeType': 'application/pdf',
            'parents':[self.shared_drive_id]
        }

        media = MediaFileUpload(filepath,
                                mimetype='application/pdf')
    
        file = self.GD_serv.files().create(body=file, media_body=media, fields='id', supportsTeamDrives=True).execute()
        print('File ID: ' + file.get('id'))
        return

    
    def help(self):
        '''
        print info about current drive service
        '''
        help_str =  "------------------------------------\n"
        help_str += "current drive id: " + self.shared_drive_id + "\n"
        help_str += "current PDF folder id: " + self.PDF_folder_id + "\n"
        help_str += "------------------------------------\n"
        print(help_str)


if __name__ == "__main__":
    serv = GDriveService()
    
    items = serv.List_All_Drive_Files()
    for f in items:
        print(f["name"], f["id"], f.get("parents"))

    print("\n")


    '''
    items = serv.List_PDF_Folder()
    for f in items:
        print(f["name"], f["id"])
    '''
    '''
    file = ""
    target = ""

    serv.copy_move(file, target)
    '''

    pdf_file = ""

    #serv.download(pdf_file,"sample.pdf")
    serv.upload("sample.pdf")
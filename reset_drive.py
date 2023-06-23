import g_drive_service
import os

#FILE DOES NOT WORK AS EXPECTED

def Move_Files_To_GDrive(local_directory):
    '''
    Moves all files from a local directory to the initial destination folders in Google Drive,
    and resets the destination folders to have a clean folder for new target files.
    '''
    # Initialize GDriveService
    serv = g_drive_service.GDriveService()

    # Get the list of files in the local directory
    files = os.listdir(local_directory)

    if files:
        for file in files:
            dest = ""
            if file == "acid.pdf":
                dest+= serv.TFA_folder_id
            elif file == "analysis1.pdf":
                dest+= serv.ANALYSIS_folder_id
            elif file == "analysis2.pdf":
                dest += serv.MACRO_folder_id
            else: 
                break
            # Create the file path
            file_path = os.path.join(local_directory, file)

            # Upload the file to the initial destination folder in Google Drive
            serv.upload(file_path, file, dest, 'PDF')
            dest = ""

        # Reset the destination folders to have a clean folder for new target files
        serv.Remove_All_Files(serv.tfa_folder_id)
        serv.Remove_All_Files(serv.ferment_folder_id)
        serv.Remove_All_Files(serv.macro_folder_id)
        serv.Remove_All_Files(serv.manure_folder_id)
        serv.Remove_All_Files(serv.other_folder_id)
        serv.Remove_All_Files(serv.dryae_folder_id)
        serv.Remove_All_Files(serv.tmr_folder_id)
        serv.Remove_All_Files(serv.grain_folder_id)
        serv.Remove_All_Files(serv.unrecognized_folder_id)

        print("All files moved to Google Drive and destination folders reset.")
    else:
        print("No files found in the local directory.")


if __name__ == "__main__":
    Move_Files_To_GDrive("unique_pdf")
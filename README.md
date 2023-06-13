# Dairy-One Extraction Scripts
#### Gordon Doore, Yiheng Su, Luis Baez
##### Last updated: 05/12/2023

This repository contains a collection of Python scripts for extracting specific data from PDF files and saving them in CSV format. The scripts utilize various libraries and methods to extract data from specific areas of the PDF files. 

TODO: fix local folders so easier to understand

## Files

- `analysis_data_extract.py`: This script extracts analysis data and sample information from a PDF file and saves them as separate CSV files. It uses the `tabula` library for PDF data extraction. Extracts files of types TMR, Manure, Dry AE, Grain, and Other.  If `sample_data[type][0]` does not match any of these, files will go to folder titled `unrecognized` when uploaded back to google drive. 

  - ##### Functions:
    - `number_of_pages(pdf_path)`: Retrieves the number of pages in a PDF file.
    - `extract_component_data(pdf_path, page)`: Extracts analysis data from a specific page of the PDF file.
    - `extract_sample_data(pdf_path, page)`: Extracts sample information from a specific page of the PDF file.
    - `extract_analysis_data_and_to_csv(pdf_path, dest_folder)`: Extracts analysis data and sample information from all pages of the PDF file and saves them as separate CSV files in the specified destination folder.

- `fermentation_data_extract.py`: This script extracts fermentation data from a PDF file and saves it as a CSV file. It utilizes the `tabula` library for PDF data extraction.

  - ##### Functions:
    - `number_of_pages(pdf_path)`: Retrieves the number of pages in a PDF file.
    - `extract_fermentation_data(pdf_path, page)`: Extracts fermentation data from a specific page of the PDF file.
    - `extract_sample_data(pdf_path, page)`: Extracts sample data from a specific page of the PDF file.
    - `extract_fermentation_data_and_to_csv(pdf_path, dest_path)`: Extracts fermentation data from all pages of the PDF file and saves it as a CSV file in the specified destination folder.

- `macros_data_extract.py`: This script extracts macros data from a PDF file and saves it as a CSV file. It uses the `tabula` library for PDF data extraction.

  - Functions:
    - `number_of_pages(pdf_path)`: Retrieves the number of pages in a PDF file.
    - `extract_macros_data(pdf_path, page)`: Extracts macros data from a specific page of the PDF file.
    - `extract_sample_data(pdf_path, page)`: Extracts sample data from a specific page of the PDF file.
    - `extract_macros_data_and_to_csv(pdf_path, dest_path)`: Extracts macros data from all pages of the PDF file and saves it as a CSV file in the specified destination folder.

- `tfa_data_extract.py`: This script extracts TFA (Total Fatty Acid) data from a PDF file and saves it as a CSV file. It utilizes the `tabula` library for PDF data extraction.

  - ##### Functions:
    - `extract_tfa_data(pdf_path, page)`: Extracts TFA data from a specific page of the PDF file.
    - `extract_sample_data(pdf_path, page)`: Extracts sample data from a specific page of the PDF file.
    - `extract_tfa_data_and_to_csv(pdf_path, dest_path)`: Extracts TFA data from all pages of the PDF file and saves it as a CSV file in the specified destination folder.

- `g_drive_service.py`: This script defines a class for interacting with Google Drive. It defines functions for authentication, file uploading, and file downloading. The script uses the Google Drive API and requires proper setup and authentication to access Google Drive.

  - ##### Functions:
    -`GDriveService()`: constructor, initializes file id's
    - `List_ALL_Drive_Files(self)`: Lists all files within shared drive, returns a list of dictionaries, each entry in the list is a file, and that entry is a dict of all the drive api info about that file
    - `List_PDF_Folder(self, folder_name)`: lists all files in the folder located at self.PDF_folder_id. Returns a list of dictionaries, each entry in the list is a file, and that entry is a dict of all the drive api info about that file.
    - `upload_file(file_path, folder_id)`: Uploads a file to Google Drive. Takes the file path and the destination folder ID as input.
    -  `get_file_parents(self, file_id)`: returns the parents of a particular file.  useful for finding folder structures etc, and getting partent id for moving files around.
    -  `Move_File(self, file_id, target_folder_id)`: moves file at `file_id` to the location of `target_folder_id`.
    - `rename_file(self, file_id, new_title)`: changes name of file at `file_id` location.
    - `download(self, file_id, download_path)`: Downloads a file from Google Drive. Takes the file ID and the destination path as input.
    - `upload(self, filepath,name,dest_id,filetype)`: Upload the file at a given filepath to the root of the shared drive in self.shared_drive_id
    - `help(self)`: print info about current drive service.


- 'process_pdf.py: This script serves as the main entry point for processing PDF files. It provides a command-line interface for selecting the appropriate data extraction script based on the PDF content. The script prompts the user to enter the PDF path, destination folder, and the type of data to extract. It then calls the corresponding data extraction script to extract and save the data.

## USAGE

1. Install the required libraries by running pip install tabula-py PyPDF2 in your Python environment.

2. Ensure that you have the necessary PDF files available for extraction.

3. Run the process_pdf.py script and follow the instructions provided. The script will prompt you to enter the PDF path, destination folder, and the type of data to extract. Select the appropriate data extraction option based on the content of the PDF file.

4. The selected data extraction script will be executed, and the extracted data will be saved as CSV files in the specified destination folder.

5. Optionally, you can use the g_drive_service.py script to upload the extracted CSV files to Google Drive by providing the appropriate authentication and destination folder details.

###### Note: Make sure to properly set up and authenticate the Google Drive API before using the g_drive_service.py script.

Please ensure that you have the necessary dependencies installed and proper authentication configured to use the scripts effectively.
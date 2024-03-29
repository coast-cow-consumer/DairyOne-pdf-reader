# Yiheng Su

import tabula 
import pandas as pd
import numpy as np
import PyPDF2
import re
from format_sample_data import add_missing_columns
from format_sample_data import format_date_cols

sample_number = 0

def number_of_pages(pdf_path):
    reader = PyPDF2.PdfReader(open(pdf_path, mode='rb' )) #initializes reader onto pdf
    return len(reader.pages) #returns number of pages


# area is defined by https://stackoverflow.com/questions/45457054/tabula-extract-tables-by-area-coordinates
def extract_component_data(pdf_path, page):
    """
    [120,231,730, 495]: rectangle for analysis report,
    [115, 21, 237, 230]: rectangle for sample information
    """
    raw_analysis = tabula.read_pdf(pdf_path, pages = page, multiple_tables=False, area=[[120,231,730, 495]], stream=True)
    # handle raw_analysis_np
    raw_analysis_np = np.array(raw_analysis)[0]
    analysis_data = []
    print(raw_analysis_np)
    for raw_datum in raw_analysis_np:
        s :list = raw_datum[0].replace(" ", "").split('|')[:3]
        if len(s) == 3 and s[0] != '':
            s.insert(0, sample_number)
            analysis_data.append(s)
    analysis_data[0][0] = 'sample number'
    analysis_data = pd.DataFrame(analysis_data[1:], columns=analysis_data[0])
    adjusted_crude_protein_row = analysis_data[analysis_data['Components'].str.contains('AdjustedCrudeProtein', regex=True)].index.max()

    #fixing column recognition issue with adjusted crude protein
    if adjusted_crude_protein_row:
        numeric_value = re.findall("\d*\.\d*", analysis_data.iloc[adjusted_crude_protein_row, 1])  # Find the numeric value in column 2, row 2
        text = re.findall("[^\d*\.\d*]", analysis_data.iloc[adjusted_crude_protein_row,1])
        text = ''.join(text[1:21])
        analysis_data.iloc[adjusted_crude_protein_row,1] = text
        analysis_data.iloc[adjusted_crude_protein_row, 3] = analysis_data.iloc[adjusted_crude_protein_row, 2]  # Assign the value from column 3 to column 4
        if len(numeric_value)>0:
            analysis_data.iloc[adjusted_crude_protein_row,2] = float(numeric_value[0])  # Convert the numeric value to a double and assign to column 3
        else:
            analysis_data.iloc[adjusted_crude_protein_row,2] = 0

    print(analysis_data)
    # return
    return analysis_data


def extract_sample_data(pdf_path, page):
    global sample_number
    raw_sample_info1 = tabula.read_pdf(pdf_path, pages = page, multiple_tables=False, area=[30, 231, 103, 495], stream=True)
    raw_sample_info2 = tabula.read_pdf(pdf_path, pages = page, multiple_tables=False, area=[116, 28, 237, 237], stream=True)
    raw_sample_info3 = tabula.read_pdf(pdf_path,pages = page, multiple_tables=False, area = [400,25,650,233], stream= True)

    #retreive comments

    arr = np.array(raw_sample_info3)
    string = ""
    if arr.shape[0] != 0:
        arr = arr.reshape((arr.shape[1],))
        for element in arr:
            string+=element+" "
        

    # handle raw_sample_info1_np
    raw_sample_info1_np = np.array(raw_sample_info1)[0]
    temp = raw_sample_info1_np[1][0].replace(" ", "").split('|')[:4]
    temp.append(raw_sample_info1_np[3][0][:-1])
    sample_info1_data = np.array(temp).reshape(1,5)
    sample_number = sample_info1_data[0][3]
    sample_info1_data = pd.DataFrame(sample_info1_data, columns=['sample description', 'farm', 'code', 'sample number', 'kind'])

    # handle raw_sample_info2_np
    raw_sample_info2_np = np.array(raw_sample_info2)[0]
    temp = raw_sample_info2_np[1][0].replace(" ", "").split('|')[1:6]
    temp.append(raw_sample_info2_np[3][0])
    name_and_address = ''
    for s in raw_sample_info2_np[4:]:
        name_and_address += s[0]
    temp.append(name_and_address)
    sample_info2_data = np.array(temp).reshape(1,7)
    sample_info2_data = pd.DataFrame(sample_info2_data, columns=['date_sampled', 'date_received', 'date_printed', 'ST', 'CO', 'type', 'name and address'])

    sample_data = pd.concat([sample_info1_data, sample_info2_data], axis=1)
   
    institution  = sample_data['name and address'][0].split('-')[0]
    investigator = sample_data['name and address'][0].split('-')[1].split('|')[0]
    sample_data[['institution','investigator']] = [institution, investigator]
    if string == "":
        string = "None"
    sample_data['comments']= [string]
    sample_data.drop('name and address', axis = 1, inplace = True)

    sample_data[['date_sampled', 'date_received', 'date_printed']]=sample_data[['date_sampled', 'date_received', 'date_printed']].replace("","01/01/2001")
    sample_data[['date_sampled', 'date_received', 'date_printed']]=sample_data[['date_sampled', 'date_received', 'date_printed']].fillna("01/01/2001")

    sample_data[['ST','CO','institution']]=sample_data[['ST','CO','institution']].replace("","None")
    sample_data[['ST','CO','institution']]=sample_data[['ST','CO','institution']].fillna("None")
    return sample_data


def extract_analysis_data_and_to_csv(pdf_path, dest_folder):
    global sample_number
    PAGE = number_of_pages(pdf_path)
    for i in range(PAGE):
        page_n =  i+1
        sample_data = extract_sample_data(pdf_path, page_n)
        analysis_data = extract_component_data(pdf_path, page_n)

        type = sample_data['type'][0].split(' ')[1][:-1]
        #check what sample['type'] is here and then add a suffix to name to indicate which, use this in process_pdf to decide where to upload
        if 'manure' in type.lower():
            suf = '_m'
            typestr = 'manure'
        elif 'other' in type.lower():
            suf = '_o'
            typestr = 'other'
        elif 'ae' in type.lower():
            suf = '_d'
            typestr = 'dry ae'
        elif 'tmr' in type.lower():
            suf = '_t'
            typestr = 'tmr'
        elif 'grain' in type.lower():
            suf = '_g'
            typestr = 'grain'
        else: 
            suf = '_?'
            typestr = '?'


        sample_filename = dest_folder + f'{sample_number}_s'+suf + '.csv'
        analysis_filename = dest_folder + f'{sample_number}_a'+suf + '.csv'

        #remove special characters from analysis_data and fix word formatting:
        analysis_data['Components'] = analysis_data['Components'].str.replace('%', '')  # Remove '%'
        analysis_data['Components'] = analysis_data['Components'].str.replace(r'([a-z])([A-Z])', r'\1 \2', regex = True)  # Add spaces between words
        analysis_data['Components'] = analysis_data['Components'].str.replace('PPM', 'PPM ')  # Add space after 'PPM'
        analysis_data['Components'] = analysis_data['Components'].str.replace('a NDF', 'aNDF')  # aNDF fix
        
        #set nan values to 0:
        analysis_data[['AsFed', 'DM']] = analysis_data[['AsFed', 'DM']].replace('',0)
        analysis_data[['AsFed', 'DM']] = analysis_data[['AsFed', 'DM']].replace('[^0-9\.]','', regex = True)
        analysis_data[['AsFed', 'DM']] = analysis_data[['AsFed', 'DM']].fillna(0)
        
        #analysis and sample data to separate csvs
        sample_data['sample_type'] = [typestr]
        sample_data = sample_data.drop(columns = ['kind'])
        sample_data = sample_data.rename(columns = {'sample description':'kind'})
        sample_data = add_missing_columns(sample_data)
        sample_data['sample_number'] = [sample_number]
        sample_data = format_date_cols(sample_data)
        sample_data.to_csv(sample_filename, index=False, na_rep = 0)
        analysis_data.to_csv(analysis_filename, index=True, na_rep= 0)
    print("PDF read Success!")


if __name__ == "__main__":
    extract_analysis_data_and_to_csv('unique_pdf/analysis1.pdf', 'unique_pdf/')
    #extract_sample_data('pdf/analysis1.pdf', 2)
    #extract_component_data('unique_pdf/analysis1.pdf', 1)

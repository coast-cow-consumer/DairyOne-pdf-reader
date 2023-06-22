# Yiheng Su, Gordon Doore

import tabula
import pandas as pd
import numpy as np
import PyPDF2
from format_sample_data import add_missing_columns

sample_number = 0

def number_of_pages(pdf_path):
    #number of pages
    reader = PyPDF2.PdfReader(open(pdf_path, mode='rb' ))
    return len(reader.pages)

def get_sample_data(pdf_path):
    global sample_number
    #tabula reads the file's header
    sample_data = tabula.read_pdf(pdf_path, pages=1, area=[144, 90, 220, 522], stream=True)[0]
    #now we want to record column names 
    column_names = sample_data.columns.tolist()
    #the column names here are actually data, so we preserve this by adding a row with the column names, then take numpy array of this df
    sample_data = pd.concat([pd.DataFrame([column_names], columns=sample_data.columns), sample_data], ignore_index=True).values
    #resize to match expected input for format_sample_data
    sample_data = np.resize(sample_data, (1, sample_data.shape[1] * sample_data.shape[0]))[0]
    #formatting code
    sample_data = format_sample_data(sample_data)
    #now extract our sample number, the global variable is updated
    sample_number = sample_data['sample_number'][0]
    sample_data['comments']=[f'Test Results for Herd {sample_number}']
    return sample_data

        


def extract_macro_data(pdf_path, page):
    """
    Captures table data on macronutrient focused files from Dairy One.
    Files must be in expected format or tabula's pixel based selection will behave as expected
    """
    if (page==1):#first page has different format so need to capture the smaller chart and avoid the header
        macro_data = tabula.read_pdf(pdf_path, pages = page, area=[245,90,760, 522], stream=True)
    else:#normal format of tables
        macro_data =  tabula.read_pdf(pdf_path, pages = page, area=[30,90,760, 522], stream=True)
    temp = np.array(macro_data)[0][1:]
    #reformat temp so no 'nan' rows 
    data = temp[::2, :]
    #second part of bname
    d1am_label = temp[1::2,1]
    #reformatting
    data[:,1] = data[:,1]+' '+d1am_label
    #make numpy array of accounts and stack into last col of temp
    account = np.ones((data.shape[0],1))*int(get_sample_data(pdf_path)['sample_number'])
    #build array of all account # so can stack and associate with each data selection
    #allows us to link sample info and sample data
    account = account.astype(int)
    data = np.hstack((data,account))
    #form pandas dataframe and return
    df =pd.DataFrame(data, columns=['sequence','bname', 'fat', 'protein', 'lactose', 'solids', 'SCC', 'MUN', 'SNF', 'sample_number'])
    
    return df

def extract_macro_data_and_to_csv(pdf_path, dest_path):
    global sample_number
    PAGE = number_of_pages(pdf_path)
    #variable for table dataframe
    macro_data = None
    for p in range(PAGE):
        #loop through each page
        #tabular has pages starting from 1 not 0, so add 1
        page_n = p + 1
        #concatanates data to same df for each page
        macro_data = pd.concat([macro_data,extract_macro_data(pdf_path, page=page_n)])
        if (p == 0):
            #if we are on the first page we want to collect and remember the sample data
            sample_data = get_sample_data(pdf_path)
        
    #when we are done adding data from each page to macro_data, we are ready to save as csv

    #formatting path
    #save data to its own file with suffix " _m"
    filename = dest_path + f'{sample_number}_m' + '.csv'
    macro_data.to_csv(filename, index=False, na_rep = 0)

    #save sample info to own file with suffix _ms title will be account#
    sample_file = dest_path +f'{sample_number}_ms'+'.csv'

    sample_data.replace('-', 0, inplace=True)
    print(sample_data)
    print(type(sample_data))
    sample_data = add_missing_columns(sample_data)
    sample_data.to_csv(sample_file, index=False, na_rep = 0)

    #finished
    print("Success!")

def format_sample_data(sample_data):
   #formats the sample data collected using tabular on the top portion of the text
    toFrame = []
    #loop through each item in sample_data
    for i, info in enumerate(sample_data):
        #i== 0, i==2, and i==6 do not need to be changed so we can just appned those in
        if i == 0 or i == 2 or i == 6:
            toFrame.append(info)
        if type(info) == str:
            #here we need to cut off the title so everything looks good
            if info.startswith('Date Sampled'):
                toFrame.append(info.split(' ')[2])
            elif info.startswith('Date Received'):
                toFrame.append(info.split(' ')[2])
            elif info.startswith('Date Analyzed'):
                toFrame.append(info.split(' ')[2])
            elif info.startswith('Account'):
                toFrame.append(info.split(' ')[1])
    #additionally, we need to rearrange columns so its in an intelligent ordering
    received = toFrame.pop(1)
    toFrame.insert(2, received)
    toFrame.append('none')
    
    #finally we convert to an array, then dataframe
    array = np.array(toFrame).reshape((1, 8))

    df = pd.DataFrame(array, columns=['investigator', 'address1', 'date_sampled', 'date_received', 'date_analyzed','address2', 'sample_number', 'comments'], dtype=str)
    df = df[['investigator', 'address1', 'address2', 'date_sampled', 'date_received', 'date_analyzed', 'sample_number', 'comments']]
    return df

    

if __name__ == "__main__":
    extract_macro_data_and_to_csv('pdf/analysis2.pdf', '')
    #extract_macro_data('analysis2.pdf', 2)
    # data = get_sample_data('pdf/analysis2.pdf')
    # print(data)

        

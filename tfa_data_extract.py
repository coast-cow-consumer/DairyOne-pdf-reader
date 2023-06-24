# Yiheng Su

import tabula
import pandas as pd
import numpy as np
import datetime
from format_sample_data import add_missing_columns
from format_sample_data import format_date_cols

sample_number = 0

def extract_tfa_data(pdf_path):
    """
    The first area extracts the table information and the second area extracts the acid data
    return table_data and acid_data
    (top,left,bottom,right)
    """
    tfa_data = tabula.read_pdf(pdf_path, pages = 'all', area=[216,30,540, 700], stream=True)
    
    current_data = []
    temp = np.array(tfa_data)[0]
    for i in range(len(temp)):
        row = temp[i]
        row = list(row)
        if ':' in row[0]:
            carbon = row[0][:5]
            name = row[0][5:]
            row[0] = name
            row.insert(1, carbon)
            current_data.append(row)
        else:
            row.insert(1,np.nan)
            current_data.append(row)
            

    # check if the data are scripted correctly
    # check if total is 100
    fatty_acid_percent = temp[:,1][:-5]

    if sum(fatty_acid_percent) > 101 or sum(fatty_acid_percent) < 99:
        print("Sum of total Fatty Acids is not 100.")
        exit()

    df = pd.DataFrame(current_data, columns=['Fatty Acid', 'Carbon', 'Percent of Total Fatty Acids', 'Percent of Dry Matter'])
    
    return df


def extract_sample_data(pdf_path):
    global sample_number
    """
    The first area extracts the table information and the second area extracts the acid data
    return table_data and acid_data
    (top,left,bottom,right)
    """
    data = tabula.read_pdf(pdf_path, pages = 'all', area=[70,300,216, 700], stream=True)
    columns = np.array(data)[0].T[0]

    for i in range(len(columns)):
        columns[i] = columns[i][:-1].lower()
    
    data = np.array(np.array(data)[0].T[1]).reshape(1,7)
    sample_number = data[0][0]
    
    sample_data = pd.DataFrame(data, columns=columns)

    sample_data.rename(columns={'sample number': 'sample_number','date sampled': 'date_sampled', 'date received':'date_received', 'date mailed':'date_mailed', 'statement id':'statement_id'}, inplace=True)

    sample_data[['date_sampled','date_received', 'date_mailed']] = sample_data[['date_sampled','date_received', 'date_mailed']].fillna("01/01/0001")
    # Convert the date format for 'date_sampled', 'date_received', and 'date_mailed' columns
    sample_data['date_sampled'] = sample_data['date_sampled'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d'))
    sample_data['date_received'] = sample_data['date_received'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d'))
    sample_data['date_mailed'] = sample_data['date_mailed'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d'))
    return sample_data

def extract_tfa_data_and_to_csv(pdf_path, dest_path):
    acid_data = extract_tfa_data(pdf_path)
    sample_data = extract_sample_data(pdf_path)
    
    concat_data = pd.concat([sample_data['sample_number'], acid_data], axis=1)
    filename = dest_path + f'{sample_number}_t' + '.csv'
    concat_data.to_csv(filename, index=True, na_rep = 0)

    sample_data[['date_sampled', 'date_received', 'date_mailed']] = sample_data[['date_sampled', 'date_received', 'date_mailed']].fillna('01/01/0000')
    sample_data[['date_sampled', 'date_received', 'date_mailed']] = sample_data[['date_sampled', 'date_received', 'date_mailed']].replace("",'01/01/0000')

    sample_data[['kind', 'description']] = sample_data[['kind', 'description']].fillna('None')
    sample_data[['kind', 'description']] = sample_data[['kind', 'description']].replace('', 'None')

    sample_data['sample_type'] = ['TFA']

    #rename mailed to printed since other types use this language
    sample_data = sample_data.rename(columns={'date_mailed': 'date_printed'})

    sample_data['statement_id'].fillna(0, inplace = True)
    sample_data['statement_id'].replace("", 0, inplace = True)

    sample_data = add_missing_columns(sample_data)
    sample_data = format_date_cols(sample_data)

    sample_data.to_csv(dest_path+f'{sample_number}_ts.csv', index = False)


if __name__ == "__main__":
    extract_tfa_data_and_to_csv('pdf/acid.pdf','')

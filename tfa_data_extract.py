# Yiheng Su

import tabula
import pandas as pd
import numpy as np

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
    return sample_data


# def extract_tfa_data_and_to_csv_two_tables(pdf_path):
#     table_data, acid_data = extract_tfa_data(pdf_path)
#     filename = pdf_path.split('.')[0]
#     table_data_filename = filename + '_table_data.csv'
#     acid_data_filename = filename + '_acid_data.csv'

#     table_data.to_csv(table_data_filename, index=False)
#     acid_data.to_csv(acid_data_filename, index=False)


def extract_tfa_data_and_to_csv(pdf_path, dest_path):
    acid_data = extract_tfa_data(pdf_path)
    sample_data = extract_sample_data(pdf_path)
    add_data = sample_data.copy()
    num_rows = acid_data.shape[0]

    for i in range(num_rows-1):
        sample_data = pd.concat([sample_data, add_data], axis=0, ignore_index=True)

    concat_data = pd.concat([sample_data, acid_data], axis=1)
    filename = dest_path + f'{sample_number}_t' + '.csv'
    concat_data.to_csv(filename, index=True, na_rep = 0)
    print("Success!")


if __name__ == "__main__":
    extract_tfa_data_and_to_csv('acid.pdf','acid_csv/')

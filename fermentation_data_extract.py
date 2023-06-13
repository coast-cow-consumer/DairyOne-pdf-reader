# Yiheng Su

import tabula
import pandas as pd
import numpy as np
import PyPDF2

sample_number = 0

def number_of_pages(pdf_path):
    reader = PyPDF2.PdfReader(open(pdf_path, mode='rb' ))
    return len(reader.pages)


def extract_fermentation_data(pdf_path, page):
    """
    The first area extracts the table information and the second area extracts the acid data
    return table_data and acid_data
    (top,left,bottom,right)
    """
    fermentation_data = tabula.read_pdf(pdf_path, pages = page, area=[152,30,350, 700], stream=True)
    temp = np.array(fermentation_data)[0][1:]
    df = pd.DataFrame(temp, columns=['component', 'dm basis', 'goal', 'typical value for dm range'])
    
    return df


def extract_sample_data(pdf_path, page):
    global sample_number
    """
    The first area extracts the table information and the second area extracts the acid data
    return table_data and acid_data
    (top,left,bottom,right)
    """
    data = tabula.read_pdf(pdf_path, pages = page, area=[30,300,126, 700], stream=True)
    columns = ['feed type', 'statement id', 'description','sample number', 'date']
    # print(data)

    # "remove : at the end of each word"
    # for i in range(len(columns)):
    #     columns[i] = columns[i][:-1].lower()
    
    data = np.array(data)[0].T[1].reshape(1,5)
    sample_number = data[0][3]

    # print(data)
    sample_data = pd.DataFrame(data, columns=columns)
    # print(sample_data)
    return sample_data


def extract_fermentation_data_and_to_csv(pdf_path, dest_path):
    PAGE = number_of_pages(pdf_path)
    for p in range(PAGE):
        page_n = p + 1
        fermentation_data = extract_fermentation_data(pdf_path, page=page_n)
        sample_data = extract_sample_data(pdf_path,page=page_n)
        add_data = sample_data.copy()
        # print(add_data)
        num_rows = fermentation_data.shape[0]

        for i in range(num_rows-1):
            sample_data = pd.concat([sample_data, add_data], axis=0, ignore_index=True)

        concat_data = pd.concat([sample_data, fermentation_data], axis=1)
        filename = dest_path + f'{sample_number}_f' + '.csv'
        concat_data.to_csv(filename, index=True, na_rep = 0)
    print("Success!")


if __name__ == "__main__":
    extract_fermentation_data_and_to_csv('analysis2.pdf', 'ferm_csv/')

# Yiheng Su

import tabula
import pandas as pd
import numpy as np
import PyPDF2

sample_number = 0

def number_of_pages(pdf_path):
    reader = PyPDF2.PdfReader(open(pdf_path, mode='rb' ))
    return len(reader.pages)


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
    for raw_datum in raw_analysis_np:
        s :list = raw_datum[0].replace(" ", "").split('|')[:3]
        if len(s) == 3 and s[0] != '':
            s.insert(0, sample_number)
            analysis_data.append(s)
    analysis_data[0][0] = 'sample number'
    analysis_data = pd.DataFrame(analysis_data[1:], columns=analysis_data[0])
    # print(analysis_data)
    return analysis_data


def extract_sample_data(pdf_path, page):
    global sample_number
    raw_sample_info1 = tabula.read_pdf(pdf_path, pages = page, multiple_tables=False, area=[30, 231, 103, 495], stream=True)
    raw_sample_info2 = tabula.read_pdf(pdf_path, pages = page, multiple_tables=False, area=[116, 28, 237, 230], stream=True)

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
    sample_info2_data = pd.DataFrame(sample_info2_data, columns=['date sampled', 'date received', 'date printed', 'ST', 'CO', 'type?', 'name and address'])

    sample_data = pd.concat([sample_info1_data, sample_info2_data], axis=1)

    return sample_data


def extract_analysis_data_and_to_csv(pdf_path, dest_folder):
    global sample_number
    PAGE = number_of_pages(pdf_path)
    for i in range(PAGE):
        page_n =  i+1
        sample_data = extract_sample_data(pdf_path, page_n)
        analysis_data = extract_component_data(pdf_path, page_n)

        sample_filename = dest_folder + f'{sample_number}_s' + '.csv'
        analysis_filename = dest_folder + f'{sample_number}_a' + '.csv'

        sample_data.to_csv(sample_filename, index=False)
        analysis_data.to_csv(analysis_filename, index=False)
    print("PDF read Success!")


if __name__ == "__main__":
    extract_analysis_data_and_to_csv('Raw_Pdf/analysis_report1.pdf')
    extract_analysis_data_and_to_csv('Raw_Pdf/analysis_report2.pdf')

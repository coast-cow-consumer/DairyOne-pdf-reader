# DairyOne Data Extraction Tools

This project aims to extract data from three different DairyOne reports. It includes the tools scraping data from DairyOne total fatty acid reports, fermentation reports, and analysis reports.

## Description

There are three python scripts in this project. 
* The **tfa_data_extract.py** script is used to extract data from DairyOne total fatty acid reports. It will save the data as csv files to the **TFA_Data** folder. Each csv file is named in the form "{sample_number}_t.csv".
* The **fermentation_data_extract.py** script is used to extract data from DairyOne fermentation reports. It will save the data as csv files to the **Fermentation_Data** folder. Each csv file is named in the form "{sample_number}_f.csv".
* The **analysis_data_extract.py** script is used to extract data from DairyOne analysis reports. For each report, it will extract two parts of the data. The first part is the sample information. It will save the sample information data as csv files to the **Sample_Information** folder. Each csv file is named in the form "{sample_name}_s.csv". The second part is the analysis report. It will save the analysis report data as csv files to the **Analysis_Data** folder. Each csv file is named in the form "{sample_name}_a.csv".

There are five folders in this project:
* **Raw_Pdf** folder saves raw DairyOne pdfs
* **Sample_Information** folder saves csv files, which contain sample information data.
* **TFA_Data** folder saves csv files, which contain total fatty acid report data.
* **Fermentation_Data** folder saves csv files, which contain fermentation report data.
* **analysis_Data** folder saves csv files, which contain analysis report data.


## Getting Started

### Dependencies
* Python version: 3.10.7 (3.XX version should work)
* numpy
* pandas
* tabula
* PyPDF2

### Executing program

* Run **tfa_data_extract.py**. In the main function, please call the following function
```
extract_tfa_data_and_to_csv(pdf_path)
```

* Run **fermentation_data_extract.py**. In the main function, please call the following function
```
extract_fermentation_data_and_to_csv(pdf_path)
```

* Run **analysis_data_extract.py**. In the main function, please call the following function
```
extract_analysis_data_and_to_csv(pdf_path)
```


## Authors

Yiheng Su

ysu24@colby.edu

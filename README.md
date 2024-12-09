# README for DCAT-US Version 1.1 Parser   

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) <img src="https://img.shields.io/badge/json-000000?style=for-the-badge&logo=json&logoColor=white" alt="JSON" height="28"> <a href="https://creativecommons.org/licenses/by/4.0"><img src="https://licensebuttons.net/l/by/3.0/88x31.png" alt="Creative Commons 4.0 BY License" height="28"></a> 

## Link to Project  
Archive Link: <https://github.com/ptvrdy/dcat-us-v1.1-parser>  

## Tables of Contents  
A. [General Information](#a-general-information)  
B. [Sharing/Access & Policies Information](#b-sharingaccess-and-policies-information)  
C. [Data and Related Files Overview](#c-file-overview)  
D. [Software Information](#d-software-information)  
E. [File Specific Information](#e-file-specific-information)  
F. [Update Log](#f-update-log)  

## A. General Information  

**Title of Program:**  DCAT-US Version 1.1 Parser 

**Description of the Program:** This program takes CSV metadata files and transforms them into DCAT-US version 1.1 metadata files in the JSON format. Translations are based on the CSV headings. The purpose of the program is convert existing metadata to the DCAT-US schema. The program interprets 1 row as 1 DCAT-US file. This program aims to streamline DCAT-US version 1.1 metadata management by converting metadata to the DCAT-US schema with minimal user input and additions. 

**Special Features of This Program:**
1. Maps CSV headings to [DCAT-US Version 1.1](https://resources.data.gov/resources/dcat-us/), crosswalking the metadata to the DCAT-US schema.  
2. The program then translates the first row and asks the user to review to spot any mistakes or mistranslations.  
3. If the user approves the translation, the program converts each row of the input CSV to an individual DCAT-US file.  
4. The program finishes and prints "Done!"  

**Dataset Archive Link:** <https://github.com/ptvrdy/dcat-us-v1.1-parser>  

**Authorship Information:**  

>  *Co-Author Contact Information*  
>  Name: Peyton Tvrdy <a href="https://orcid.org/0000-0002-9720-4725"><img src="https://th.bing.com/th/id/OIP.8aLkQghWV6uvFMxGtFAgmwHaHa?rs=1&pid=ImgDetMain" height="19"> ([0000-0002-9720-4725](https://orcid.org/0000-0002-9720-4725))   
>  Institution: National Transportation Library [(ROR ID: https://ror.org/00snbrd52)](https://ror.org/00snbrd52)   
>  Email: [peyton.tvrdy.ctr@dot.gov](mailto:peyton.tvrdy.ctr@dot.gov)

>  *Co-Author Contact Information*  
>  Name: Joseph Lambeth  
>  Email: josephwlambeth@gmail.com  

## B. Sharing/Access and Policies Information  

**Recommended citation for the data:**  

>  Tvrdy, Peyton and Joseph Lambeth. (2024). DCAT-US Version 1.1 Parser . <https://github.com/ptvrdy/dcat-us-v1.1-parser>  

**Licenses/restrictions placed on the data:** https://creativecommons.org/licenses/by/4.0  
 
## C. File Overview  

File List for doi-parser  

>  1. Filename: `Templates`  
>  Short Description:  This folder contains a blank DCAT-US version 1 template.    

>  2. Filename: `collections_and_series.py`  
>  Short Description:  This file contains the National Transportation Library ROSA P Repository's series and collections DOIs (Digital Object Identifiers).  

>  3. Filename: `dcat-us-parser.py`   
>  Short Description:  This is the main python file that loads the CSV, conducts the transformation, and verifies the conversions.   

>  4. Filename: `LICENSE`  
>  Short Description: This is the license file.  

>  5. Filename: `processing_columns.py`  
>  Short Description: This python file contains all the conversion functions and default values for the DCAT-US conversion. These functions should be changes according to the needs of your organization.  

>  6. Filename: `README.md`  
>  Short Description:  This file is the README file you are reading now. It contains helpful background information about the program its function.  

## D. Software Information  

**Instrument or software-specific information needed to interpret the data:** This software is best run through command prompt. It is best edited with Visual Studio Code. Microsoft Excel was used to create the CSV files. To run this software, open the command prompt and navigate to the folder that contains this program. Then, type the following command:  

`python dcat-us-parser.py` + CSV file  

**Example**: 
```
python dcat-us-parser CSV_1_20241231.csv
```   


## E. File Specific Information  

1. **collections_and_series.py**  
This file contains information that is relevant to my organization, NTL. This dictionary should be changed with values that are relevant to your institution.  

2. **processing_columns.py**  
This file is where you would make adjustments to my functions and add your own. Please contact if you would like assistance adjusting this program to your needs.  

## F. Update Log  

This README.md file was originally created on 2024-12-09 by Peyton Tvrdy ([0000-0002-9720-4725](https://orcid.org/0000-0002-9720-4725)), Data Management and Data Curation Fellow, National Transportation Library <peyton.tvrdy.ctr@dot.gov>  
 
2024-12-09: Project Launch and README created  

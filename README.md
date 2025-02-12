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

**For more in-depth information about the program and how to use it, view the [Repository's Wiki](https://github.com/ptvrdy/dcat-us-v1.1-parser/wiki).**

## B. Sharing/Access and Policies Information  

**Recommended citation for the data:**  

>  Tvrdy, Peyton and Joseph Lambeth. (2024). DCAT-US Version 1.1 Parser . <https://github.com/ptvrdy/dcat-us-v1.1-parser>  

**Licenses/restrictions placed on the data:** https://creativecommons.org/licenses/by/4.0  
 
## C. File Overview  

File List for doi-parser  

>  1. Filename: `Templates`  
>  Short Description:  This folder contains a blank DCAT-US version 1 template.    

>  2. Filename: `collections_and_file_types.py`  
>  Short Description:  This file contains the National Transportation Library ROSA P Repository's series and collections DOIs (Digital Object Identifiers).  

>  3. Filename: `dcat-us-parser.py`   
>  Short Description:  This is the main python file that loads the CSV, conducts the transformation, and verifies the conversions.   

>  4. Filename: `LICENSE`  
>  Short Description: This is the license file.  

>  5. Filename: `processing_columns.py`  
>  Short Description: This python file contains all the conversion functions and default values for the DCAT-US conversion. These functions should be changes according to the needs of your organization.  

>  6. Filename: `README.md`  
>  Short Description:  This file is the README file you are reading now. It contains helpful background information about the program its function.  

>  7. Filename: `_start.bat`  
>  Short Description:  This file is a batch file that functions as a quick start for the program. Edit the file in your chosen file editor, such as VS Code, to navigate to the file path of where this program is located on your computer. This file eliminates the change directory/CD step in command prompt for quicker use.   

>  8. Filename: `distribution_quickrun.py`  
>  Short Description:  In the DCAT-US version 1 schema, the field "distribution" is a complicated field meant to describe each file in the dataset. This includes the file's title, IANA media type, file type, a description, an access URL, and the default ""@type": "dcat:Distribution"," for each file. This function is designed to take a CSV full of only file titles and map the rest of the values with default values. This is especially useful for when you have a DCAT-US file prepared for publication, but the distribution is not feasible for a human to complete in a reasonable time frame (ex: a dataset with 1000+ files). For more detailed instructions, read "distribution_quickrun.py instructions" in Section E. "File Specific Information."  

>  9. Filename: `file_definitions.json`
>  Short Description:  This file contains all the definitions from the [File Formats Dictionary LibGuide](https://transportation.libguides.com/researchdatamanagement/fileformatdictionary). It is structured in the JSON format and converted into a python dictionary by the program. It is created through the scrape.py file.  

>  10. Filename: `run_definitions_update.bat`
>  Short Description:  This file is a Windows Bat file that runs 'update_definitions.sh.' Once configured to your local instance, it offers a "one-click solution" to easily update 'file_definitions.json' if there have been any updates to the [File Formats Dictionary LibGuide](https://transportation.libguides.com/researchdatamanagement/fileformatdictionary).   

>  11. Filename: `scrape.py`
>  Short Description:  This python file scrapes [File Formats Dictionary LibGuide](https://transportation.libguides.com/researchdatamanagement/fileformatdictionary) and saves it as a JSON object called file_definitions.json.  

>  12. Filename: `update_definitions.sh`
>  Short Description:  This file runs scrape.py and creates a new, temporary file_definions.json file. If there have been any changes or additions to the [File Formats Dictionary LibGuide](https://transportation.libguides.com/researchdatamanagement/fileformatdictionary), it saves the new file as file_definitions.json, overwriting the original. Then it updates the GitHub repository with the new file_definitions.json file.  

>  13. Filename: `file_cleaup.py`
>  Short Description:  This file cleans up filename.txt files that were created in command prompt using the command "dir /s > filenames.txt." These files contain directory information, folder information, and every file name and path of the dataset package.  

**For more in-depth information about the program and how to use it, view the [Repository's Wiki](https://github.com/ptvrdy/dcat-us-v1.1-parser/wiki).**

## D. Software Information  

**Instrument or software-specific information needed to interpret the data:** This software is best run through command prompt. It is best edited with Visual Studio Code. Microsoft Excel was used to create the CSV files. To run this software, open the command prompt and navigate to the folder that contains this program. Then, type the following command:  

`python dcat-us-parser.py` + CSV file  

**Example**: 
```
python dcat-us-parser CSV_1_20241231.csv
```   

*Note: Edit the `_start.bat` file to where your program is stored to make the bat file a quick start button with no changing directories necessary.*

**For more in-depth information about the program and how to use it, view the [Repository's Wiki](https://github.com/ptvrdy/dcat-us-v1.1-parser/wiki).**

## E. File Specific Information  

1. **collections_and_file_types.py**  
This file contains information that is relevant to my organization, NTL. This dictionary should be changed with values that are relevant to your institution. For the constant values to work properly, change the collection and series DOIs and ensure that your file type is included in the "extension_metadata" dictionary. The program will pull an error if your file type is not accounted for.  

2. **processing_columns.py**  
This file is where you would make adjustments to my functions and add your own. Please contact if you would like assistance adjusting this program to your needs. To ensure the program and certain functions run properly, please read each function thoroughly.  

3. **distribution_quickrun.py Instructions**
To quickly get the distribution for a large dataset, use the following instructions.  

    1. Navigate to your dataset and open "Command Prompt"  
    2. Change directory to that dataset's main folder (ex: `cd /d C:\source\repos\dataset_1`)  
    3. Enter the following command to print every file in that folder to a plain .txt file. This will include files in subfolders, so that the entirity of the dataset is accounted for: 
    `dir /s /b > filenames.txt`  
    4. Take that entire list and paste into a plain Excel spreadsheet Values only starting with cell A1.  
    5. Remove and rows that are folders and not files.  
    6. In Cell B1, type "extension.distribution.title.1".  
    7. Autofill the rest of column B by selecting cell B1 and clicking the small box in the bottom right corner of the cell to autofill.  
    8. Double check the spreadsheet to ensure each file is accounted for and has an assigned "extension.distribution.title." + number.  
    9. Create a CSV document in Excel and open it.  
    10. Select column A and paste into the CSV row 2, making sure to paste using the "Transpose (T)" option. This should turn your 1 Column with X rows, in 1 row with X columns.   
    11. Do the same with the "extension.distribution.title.1" column B into row 1 of the CSV. The "title" column should now be row 1, and the actual file names should be row 2. Save your CSV in your version in the folder of "DCAT-US Version 1.1 parser" on your computer.  
    12. Instead of running the usual command of `python dcat-us-parser CSV_1_20241231.csv` run the command: `python distribution_quickrun.py CSV_1_20241231.csv` with the "CSV_1_20241231.csv" being the name of the CSV file you just made in command prompt.  
    13. The program will now ask you for the DOI of the dataset. Provide the DOI in the command prompt terminal.  
    14. The program will now generate the DCAT-US "distribution" field. Ensure it looks correct and that all file types are accounted for before proceeding. Upon being prompted, type "y" to verify that the information looks correct if it is correct.  
    15. The program will print "Done!" and provide you with a JSON file with only the DCAT-US "distribution" field for you to put into another DCAT-US JSON file.  

**For more in-depth information about the program and how to use it, view the [Repository's Wiki](https://github.com/ptvrdy/dcat-us-v1.1-parser/wiki).**

## F. Update Log  

This README.md file was originally created on 2024-12-09 by Peyton Tvrdy ([0000-0002-9720-4725](https://orcid.org/0000-0002-9720-4725)), Data Management and Data Curation Fellow, National Transportation Library <peyton.tvrdy.ctr@dot.gov>  
 
2024-12-09: Project Launch and README created  
2025-01-06: Small edits to file descriptions, 1 file name change  
2025-02-12: New programs (scrape,py, file_cleanup.py, file_definitions.json, and other files added. Added **[Repository's Wiki](https://github.com/ptvrdy/dcat-us-v1.1-parser/wiki).** Adjusted the README to include new files and functions.   
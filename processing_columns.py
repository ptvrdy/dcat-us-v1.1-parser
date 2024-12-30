from collections_and_series import (
    collections_to_doi_lookup,
    series_to_doi_lookup
)

import json
import logging
import re

LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s"

# This function deletes columns
def delete_unwanted(json_obj, key):
    if key in json_obj:
        del json_obj[key]

# This function removes all unnecessary columns from the standard metadata export spreadsheet
def delete_unwanted_columns(json_list):
    for index, json_obj in enumerate(json_list):
        delete_unwanted(json_obj, "DOCID")
        delete_unwanted(json_obj, "Primary URL")
        delete_unwanted(json_obj, "Alternate URL(s)")
        delete_unwanted(json_obj, "Personal Creator(s)")
        delete_unwanted(json_obj, "Personal Contributor(s)")
        delete_unwanted(json_obj, "Corp.Creator(s)")
        delete_unwanted(json_obj, "Corp.Contributor(s)")
        delete_unwanted(json_obj, "Classification")
        delete_unwanted(json_obj, "Subject Keywords")
        delete_unwanted(json_obj, "Alternate Title")
        delete_unwanted(json_obj, "Personal Publisher(s)")
        delete_unwanted(json_obj, "Publication Year")
        delete_unwanted(json_obj, "Publication Month")
        delete_unwanted(json_obj, "Publication Day")
        delete_unwanted(json_obj, "Language")
        delete_unwanted(json_obj, "Resource Type (NTL)")
        delete_unwanted(json_obj, "Source")
        delete_unwanted(json_obj, "Table of Contents")
        delete_unwanted(json_obj, "TRIS")
        delete_unwanted(json_obj, "OCLC")
        delete_unwanted(json_obj, "ISBN")
        delete_unwanted(json_obj, "ISSN")
        delete_unwanted(json_obj, "Distribution Hold Start Date")
        delete_unwanted(json_obj, "Distribution Hold End Date")
        delete_unwanted(json_obj, "Copyright Date")
        delete_unwanted(json_obj, "Date Captured")
        delete_unwanted(json_obj, "Copyright")
        delete_unwanted(json_obj, "Contract Number(s)")
        delete_unwanted(json_obj, "Contracting Officer")
        delete_unwanted(json_obj, "Report Number(s)")
        delete_unwanted(json_obj, "Edition")
        delete_unwanted(json_obj, "Supplier")
        delete_unwanted(json_obj, "Staff Notes")
        delete_unwanted(json_obj, "Status")
        delete_unwanted(json_obj, "Status Comment")
        delete_unwanted(json_obj, "Date Modified")
        delete_unwanted(json_obj, "Modified By")
        delete_unwanted(json_obj, "Date Created")
        delete_unwanted(json_obj, "Created By")
        delete_unwanted(json_obj, "Comment Date")
        delete_unwanted(json_obj, "Comment By")
        delete_unwanted(json_obj, "Is Version of")
        delete_unwanted(json_obj, "Contains")
        delete_unwanted(json_obj, "Is Format Of")
        delete_unwanted(json_obj, "Requires")
        delete_unwanted(json_obj, "References")
        delete_unwanted(json_obj, "Preceding Entry")
        delete_unwanted(json_obj, "Rosap ID")
        logging.info(f"All unnecessary columns deleted for row {index+1}.")
    return json_list

# This function takes the "Title" in the spreadsheet and matches it to "title"
def title(json_list):
    for index, json_obj in enumerate(json_list):
        if "Title" in json_obj:
            title = json_obj.pop("Title")
            json_obj.setdefault("title", title,)
        else:
            logging.warn(f"Title not found for row {index+1}.")
    logging.info(f"Title mapped for row {index+1}.")
    return json_list

# This function takes the "TRT Term(s)" in the spreadsheet and matches it to "keyword"
def keywords(json_list):
    for index, json_obj in enumerate(json_list):
        if "TRT Term(s)" in json_obj:
            keywords_str = json_obj.pop("TRT Term(s)")
            if keywords_str.endswith(", "):
                keywords_str = keywords_str[:-2]
            keywords_list = keywords_str.split("\n")
            json_obj.setdefault("keyword", keywords_list)
        else:
            logging.info(f"TRT Terms not found for row {index+1}.")
    logging.info(f"Keywords mapped for row {index+1}..")
    return json_list

# This function matches "Publication Date" in the spreadsheet to "issued" and "modified" dates
def publication_date(json_list):
    for index, json_obj in enumerate(json_list):
        if "Publication Date" in json_obj:
            date = json_obj.pop("Publication Date")
            json_obj.setdefault("issued", date)
            json_obj.setdefault("modified", date)
        else:
            logging.warn(f"Date not found for row {index+1}.")
    logging.info(f"Publication Date mapped for row {index+1}..")
    return json_list

# This function matches "Geographical Coverage" to "spatial" and defaults to "United States" if empty
def geographical_coverage(json_list):
    for index, json_obj in enumerate(json_list):
        if json_obj.get("Geographical Coverage"):
            spatial = json_obj.pop("Geographical Coverage")
            json_obj.setdefault("spatial", spatial)
        else:
            json_obj.setdefault("spatial", "United States")
    logging.info(f"Geographic Information mapped for row {index+1}.")
    return json_list

# This function matches "Format (NTL)" in the spreadsheet to "format"
def file_formats(json_list):
    for index, json_obj in enumerate(json_list):
        if "Format (NTL)" in json_obj:
            file = json_obj.pop("Format (NTL)")
            json_obj.setdefault("format", file)
        else:
            logging.info(f"File Format not found for row {index+1}.")
    logging.info(f"File format mapped for row {index+1}.")
    return json_list

# This function matches the "Abstract" in the spreadsheet to "description"
def abstract(json_list):
    for index, json_obj in enumerate(json_list):
        if "Abstract" in json_obj:
            description = json_obj.pop("Abstract")
            json_obj.setdefault("description", description)
        else:
            logging.info(f"Abstract not found for row {index+1}.")
    logging.info(f"Abstract mapped for row {index+1}.")
    return json_list

# This function matches "Digital Object Identifier" in the spreadsheet to "identifier"
def digital_object_identifier(json_list):
    for index, json_obj in enumerate(json_list):
        if "Digital Object Identifier" in json_obj:
            objectDOI = json_obj.pop("Digital Object Identifier")
            json_obj.setdefault("identifier", objectDOI)
        else:
            logging.info(f"DOI not found for row {index+1}.")
            if not json_obj.get("Rosap URL"):
                rosap_url(json_list)
            json_obj.setdefault("identifier", json_obj["Rosap URL"])
    logging.info(f"DOI mapped for row {index+1}.")
    return json_list

# This function matches "Collections" in the spreadsheet to the collections DOI list in the collections_and_series.py file and then to "isPartOf"
def collections(json_obj, index):
    if "Collections" in json_obj:
        collection = json_obj.pop("Collections")
        collection = collection.strip()
        if collection in collections_to_doi_lookup:
            json_obj.setdefault("isPartOf", collections_to_doi_lookup[collection])
    else:
        logging.info(f"Collection not found for row {index+1} in collection lookup.")

# This function matches "Is Part Of" in the spreadsheet to the series DOI list in the collections_and_series.py file and then to "isPartOf"
def series(json_list):
    for index, json_obj in enumerate(json_list):
        if json_obj.get("Is Part of"):
            series = json_obj.pop("Is Part of")
            series = series.strip()
            if series in series_to_doi_lookup:
                json_obj.setdefault("isPartOf", series_to_doi_lookup[series])
                json_obj.pop("Collections")
            else:
                logging.info(f"Series not found in lookup for row {index+1}.")
                collections(json_obj, index)
        else:
            logging.info(f"No series found for row {index+1}. Using collection DOI instead.")
            collections(json_obj, index)
    logging.info(f"Series mapped for row {index+1}.")
    return json_list

# This function matches the ROSA P Url in the spreadsheet to "landingPage"
def rosap_url(json_list):
    for index, json_obj in enumerate(json_list):
        if "Rosap URL" in json_obj:
            landing = json_obj.pop("Rosap URL")
            json_obj.setdefault("landingPage", landing)
        else:
            logging.info(f"No ROSA P URL found for row {index+1}.")
    logging.info(f"ROSA P URL mapped for row {index+1}.")
    return json_list

# This function breaks down "Corp. Publisher(s)", splitting at the "." and nests it into the "publisher" DCAT-US structure
def publisher(json_list):
    for index, json_obj in enumerate(json_list):
        if "Corp. Publisher(s)" in json_obj:
            publisher_str = json_obj.pop("Corp. Publisher(s)").split("\n", 1)[0]
            publisher_str = publisher_str.strip()
            publisher_list = publisher_str.split(".")
            logging.info(f"Publisher list before reversal: {publisher_list}")
            json_obj["publisher"] = recursive_func(publisher_list[::-1])
            logging.info(f"Publisher mapped successfully: {json_obj['publisher']} for row {index+1}.")
    return json_list
            

def recursive_func(publisher_list):
    if len(publisher_list) == 0:
        return None  # Base case: no more publishers to process
    
    my_obj = {
        "@type": "org:Organization",
        "name": publisher_list[0],
    }
    
    # Recursively call for the rest of the list
    sub_org = recursive_func(publisher_list[1:])
    if sub_org:  # Only add "subOrganizationOf" if there is a sub-organization
        my_obj["subOrganizationOf"] = sub_org
    
    return my_obj


###################################################################
###################################################################
####    Additional Optional Fields Added by User Start Here   #####
###################################################################
###################################################################

def distribution(json_list):
    for index, json_obj in enumerate(json_list):
        parsed_doi = json_obj["identifier"]
        
        # Regex pattern to match the title keys
        title_pattern = re.compile(r"extension\.distribution\.title\.(\d+)")
        
        # Collect keys matching the pattern
        title_keys = [key for key in json_obj.keys() if title_pattern.match(key)]
        
        for key in title_keys:
            match = title_pattern.match(key)
            if match:
                distribution_index = match.group(1)  # Extract the number after 'title.'
                title = json_obj[key]  # Get the file name
                
                # Create a distribution object
                distribution_obj = {
                    "@type": "dcat:Distribution",
                    "accessURL": parsed_doi,
                    "title": title,
                }
                
                # Extract the file extension and assign metadata
                extension = title.split(".")[-1].lower()
                if extension == "csv":
                    distribution_obj["format"] = "CSV"
                    distribution_obj["mediaType"] = "text/csv"
                    distribution_obj["description"] = "CSV dataset file."
                elif extension == "txt":
                    distribution_obj["format"] = "TXT"
                    distribution_obj["mediaType"] = "text/plain"
                    distribution_obj["description"] = "Plain text file."
                elif extension == "pdf":
                    distribution_obj["format"] = "PDF"
                    distribution_obj["mediaType"] = "application/pdf"
                    distribution_obj["description"] = "PDF files for dataset."
                elif extension == "xlsx":
                    distribution_obj["format"] = "XLSX"
                    distribution_obj["mediaType"] = "application/vnd.ms-excel"
                    distribution_obj["description"] = "XLSX dataset files for the project."
                elif extension == "md":
                    distribution_obj["format"] = "MD"
                    distribution_obj["mediaType"] = "text/markdown"
                    distribution_obj["description"] = "Markdown documentation file for the dataset."
                elif extension == "pptx":
                    distribution_obj["format"] = "PPTX"
                    distribution_obj["mediaType"] = "application/vnd.ms-powerpoint"
                    distribution_obj["description"] = "PowerPoint file for the project."
                elif extension == "docx":
                    distribution_obj["format"] = "DOCX"
                    distribution_obj["mediaType"] = "application/msword"
                    distribution_obj["description"] = "Microsoft Word documentation file for the dataset."
                elif extension == "cpg":
                    distribution_obj["format"] = "CPG"
                    distribution_obj["mediaType"] = "application/octet-stream"
                    distribution_obj["description"] = "GIS project component file."
                elif extension == "dbf":
                    distribution_obj["format"] = "DBF"
                    distribution_obj["mediaType"] = "application/dbf"
                    distribution_obj["description"] = "GIS project component file."
                elif extension == "prj":
                    distribution_obj["format"] = "PRJ"
                    distribution_obj["mediaType"] = "application/octet-stream"
                    distribution_obj["description"] = "This file contains projection information for GIS datasets."
                elif extension == "sbn":
                    distribution_obj["format"] = "SBN"
                    distribution_obj["mediaType"] = "application/octet-stream"
                    distribution_obj["description"] = "This file is associated with spatial index files for Esri shapefiles."
                elif extension == "sbx":
                    distribution_obj["format"] = "SBX"
                    distribution_obj["mediaType"] = "application/octet-stream"
                    distribution_obj["description"] = "This file is associated with spatial index files for Esri shapefiles."
                elif extension == "shp":
                    distribution_obj["format"] = "SHP"
                    distribution_obj["mediaType"] = "application/x-esri-shapefile"
                    distribution_obj["description"] = "This file represents the actual geometries of a shapefile dataset."
                else:
                    logging.warn(f"Format not mapped for {title}.")
                
                # Add the distribution object to the json_obj
                json_obj.setdefault("distribution", []).append(distribution_obj)
                logging.info(f"Distribution mapped for title key {key} in row {index+1}.")
                
        # Remove the title keys from the JSON object
        for key in title_keys:
            del json_obj[key]
    return json_list
                
                
def references(json_list):
    for index, json_obj in enumerate(json_list):
        logging.info(f"Starting references for row {index+1}.")
        if "extension.References" in json_obj:
            references_str = json_obj.pop("extension.References")
            if references_str.endswith(", "):
                references_str = references_str[:-2]
            references_list = references_str.split("\n")
            json_obj.setdefault("references", references_list)
            logging.info(f"References mapped for row {index+1}.")
        else:
            logging.info(f"No references found for row {index+1}.")
    return json_list

###################################################################
###################################################################
################    Autofill Columns Start Here   #################
###################################################################
###################################################################

# This function will autofill default values that are true for every USDOT DCAT-US file
def autofillColumns(json_list):
    for json_obj in json_list:
        json_obj["language"] = ["en-US"]
        json_obj["@type"] = "dcat:Dataset"
        json_obj["accessLevel"]= "public"
        json_obj["bureauCode"] = ["021:04"]
        json_obj["contactPoint"] = {
            "fn": "National Transportation Library Data Curator", 
            "hasEmail": "mailto:NTLDataCurator@dot.gov", 
            "@type": "vcard:Contact"}
        json_obj["dataQuality"] = True
        json_obj["license"] = "https://creativecommons.org/publicdomain/zero/1.0/"
        json_obj["policyStatement"] = "This dataset was made public under the requirements enumerated in the U.S. Department of Transportation's 'Plan to Increase Public Access to the Results of Federally-Funded Scientific Research' Version 1.1 << https://doi.org/10.21949/1520559 >> and guidelines suggested by the DOT Public Access website << https://doi.org/10.21949/1503647  >>, in effect and current as of December 03, 2020."
        json_obj["policyURL"] = "https://doi.org/10.21949/1520559 , https://doi.org/10.21949/1503647"
        json_obj["programCode"] = ["021:053"]
        json_obj["rights"] = "This resource was created or funded by the United States Department of Transportation. Use of this resource is unrestricted to the public."
        json_obj["webService"] = None
    return json_list

###################################################################
###################################################################
###########   Wrapping Headers onto each DCAT-US File   ###########
###################################################################
###################################################################

# This function wraps each dcat object with the necessary headings
def wrap_object(json_list):
    output_list = list()
    for json_obj in json_list:
        output_obj = {"$schema": "https://resources.data.gov/schemas/dcat-us/v1.1/schema/catalog.json", 
                      "conformsTo": "https://project-open-data.cio.gov/v1.1/schema",
                      "@type": "dcat:Catalog",
                      "@context": "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld",
                      "dataset": [json_obj]}
        output_list.append(output_obj)
        logging.info(f"All objects wrapped.")
    return output_list
import codecs
import csv
import json
import logging
import re
import sys

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARN)

LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s"

logging.basicConfig(handlers=[stream_handler],
					level=logging.INFO,
                    format=LOG_FORMAT)

# This is where your input csv is read, each row is equal to 1 DCAT-US JSON file
def read_csv_file(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        rows = [row[0].strip() for row in csv_reader if row]
    return rows

# This function converts the CSV file to JSON
def csv_to_json(csv_reader):
    output = []
    header_row = True
    keys = {}
    
    for row in csv_reader:
        if header_row:
            logging.info("===> Parsing CSV")
            row[0] = row[0].strip(codecs.BOM_UTF8.decode('utf-8'))
            keys = {i: row[i].strip() for i in range(len(row)) if row[1].strip()} 
            header_row = False
            continue
        
        output_obj = {}
        for i in range(len(keys)):
            key = keys[i]
            element = row[i].strip() if i < len(row) else ''
            if element:
                output_obj[key] = element
                
        if output_obj:
            output.append(output_obj)
            
    return output


def main():
    # If user doesn't select a CSV
    if len(sys.argv) != 2:
        file_handler = logging.FileHandler('default_process.log')
        logging.getLogger().addHandler(file_handler)
        file_handler.setLevel(logging.INFO)
        logging.error(f"Error: Please provide a filename")
        sys.exit(1)
        
    # This changes the log names so that the log is named after the input file
    log_filename = sys.argv[1].rstrip('csv') + 'log'
    local_file_handler = logging.FileHandler(log_filename)
    local_file_handler.setLevel(logging.INFO)
    local_file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(local_file_handler)
    
    try:
        print(f"\n===============================================================================================================")
        print(f"                                         Welcome to DCAT-US Parser!                                       ")
        print(f"===============================================================================================================")
        
        logging.info(f"====> Starting File Reader: {sys.argv[1]}")
        print(f"\n\n====> Starting File Reader: {sys.argv[1]}")
        
        with open(sys.argv[1], 'r', encoding='utf-8') as fp:
            csv_reader = csv.reader(fp)
            output = csv_to_json(csv_reader)
            
        # Initialize processing
        print(f"\n\n\n\n====> Now beginning transformation processes...")
        output = distribution(output)
        

        logging.info("===> Finished Parsing\n")

        # Display the first JSON object with custom formatting for verification
        print(json.dumps(output[0], indent=4))
        should_continue = input(f"\n====> Does the above look good? [y/N]: ").upper() == 'Y'

        if not should_continue:
            print(f"Aborting...")
            sys.exit(2)

        # Loop through each row and create a separate JSON file for each
        i = 0
        for obj in output:  # Iterate over the output directly
            print(obj)
            title = "Untitled" + str(i)  # Use "Untitled" if there's no title field
            title_safe = title.replace(" ", "_").replace("/", "_").replace("\\", "_")  # Clean the title for filenames


            out_filename_json = f"{title_safe}"  # Create the filename based on the title
            if '.json' not in out_filename_json:
                 out_filename_json += '.json'
            logging.info(f"\n\n====> Starting Output Write: %s " % out_filename_json)
            print(f"\n\n====> Starting Output Write: %s " % out_filename_json)

            # Write each item as a separate JSON file
            with open(out_filename_json, "w") as fpo:
                formatted_json = json.dumps(obj, indent=4)
                fpo.write(formatted_json)
            i += 1

        logging.info(f"\n====> Done !")
        print(f"\n====> Done !")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


def distribution(json_list):
    for index, json_obj in enumerate(json_list):
        identifier = input(f"\n====> What is the DOI for the dataset?: ")
        
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
                    "accessURL": identifier,
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
                elif extension == "shx":
                    distribution_obj["format"] = "SHX"
                    distribution_obj["mediaType"] = "application/octet-stream"
                    distribution_obj["description"] = "This file is associated with spatial index files for Esri shapefiles."
                elif extension == "xml":
                    distribution_obj["format"] = "XML"
                    distribution_obj["mediaType"] = "test/xml"
                    distribution_obj["description"] = "This file contains information about the dataset."
                else:
                    logging.warn(f"Format not mapped for {title}.")
                
                # Add the distribution object to the json_obj
                json_obj.setdefault("distribution", []).append(distribution_obj)
                logging.info(f"Distribution mapped for title key {key} in row {index+1}.")
                
        # Remove the title keys from the JSON object
        for key in title_keys:
            del json_obj[key]
    return json_list



if __name__ == '__main__':
	main()
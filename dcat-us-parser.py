import codecs
import csv
import json
import logging
import processing_columns
from processing_columns import *
import sys

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARN)

logging.basicConfig(handlers=[stream_handler],
					level=logging.INFO,
                    format=processing_columns.LOG_FORMAT)

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
    local_file_handler.setFormatter(logging.Formatter(processing_columns.LOG_FORMAT))
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
        output = do_column_processes(output)
        print(f"\n\n\n\n====> Now beginning transformation processes...")

        logging.info("===> Finished Parsing\n")

        def format_json_with_custom_sort(obj):
            """Sort JSON object with custom logic."""
            # Sort the elements inside the "dataset" field if it exists
            if "dataset" in obj:
                sorted_dataset = [
                    json.loads(json.dumps(item, sort_keys=True))  # Sort keys within each dataset object
                    for item in obj["dataset"]
                ]
                obj["dataset"] = sorted_dataset

            # Sort the entire object while keeping "dataset" as-is
            sorted_obj = json.loads(json.dumps(obj, sort_keys=True))
            return sorted_obj

        # Display the first JSON object with custom formatting for verification
        titles = {}
        for json_obj in output:
            titles[json_obj["dataset"][0]['identifier']] = json_obj["dataset"][0].pop('extension.outputfile')
        print(json.dumps(format_json_with_custom_sort(output[0]), indent=4))
        should_continue = input(f"\n====> Does the above look good? [y/N]: ").upper() == 'Y'

        if not should_continue:
            print(f"Aborting...")
            sys.exit(2)

        # Loop through each row and create a separate JSON file for each
        for obj in output:  # Iterate over the output directly
            title = titles.get(obj["dataset"][0]["identifier"], "Untitled")
            title_safe = title.replace(" ", "_").replace("/", "_").replace("\\", "_")  # Clean the title for filenames


            out_filename_json = f"{title_safe}"  # Create the filename based on the title
            if '.json' not in out_filename_json:
                 out_filename_json += '.json'
            logging.info(f"\n\n====> Starting Output Write: %s " % out_filename_json)
            print(f"\n\n====> Starting Output Write: %s " % out_filename_json)

            # Write each item as a separate JSON file
            with open(out_filename_json, "w") as fpo:
                formatted_json = json.dumps(format_json_with_custom_sort(obj), indent=4)
                fpo.write(formatted_json)

        logging.info(f"\n====> Done !")
        print(f"\n====> Done !")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


        
def do_column_processes(output):
    for func in (delete_unwanted_columns,
                 title,
                 keywords,
                 publication_date,
                 geographical_coverage,
                 file_formats,
                 abstract,
                 digital_object_identifier,
                 series,
                 rosap_url,
                 publisher,
                 distribution,
                 references,
                 autofillColumns,
                 wrap_object):
        
        output = func(output)
    return output


if __name__ == '__main__':
	main()
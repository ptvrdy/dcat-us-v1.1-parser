import pandas as pd
import re

# Define input and output filenames
input_file = "filenames.txt"
output_file = "filenames.csv"

# List to store extracted filenames
file_list = []

# Regular expression pattern to match valid file entries
file_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2} [APM]+\s+\d{1,3}(?:,\d{3})*\s+(.+\..+)$')

# Read the file line by line
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        match = file_pattern.match(line.strip())
        if match:
            filename = match.group(1)
            # Exclude .zip files and "filenames.txt"
            if not filename.lower().endswith(".zip") and filename.lower() != "filenames.txt":
                file_list.append(filename)

# Generate column headers like "extension.distribution.title.1", "extension.distribution.title.2", etc.
headers = [f"extension.distribution.title.{i+1}" for i in range(len(file_list))]

# Convert to DataFrame (single row of filenames)
df = pd.DataFrame([file_list], columns=headers)

# Save as CSV
df.to_csv(output_file, index=False)

print(f"Extracted {len(file_list)} filenames and saved to {output_file}.")

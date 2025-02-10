import requests
from bs4 import BeautifulSoup
import re

# URL of your LibGuide
URL = "https://transportation.libguides.com/researchdatamanagement/fileformatdictionary"

# Fetch the page content
response = requests.get(URL)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract text content and clean up non-breaking spaces
text_content = soup.get_text().replace("\u00a0", " ")

# Initialize an empty dictionary
file_definitions = {}

# Regex pattern to match file extensions and their definitions
pattern = re.compile(r"(?P<extension>\.\w+):\s(?P<description>.+)")

# Process each line of the extracted text
for line in text_content.split("\n"):
    match = pattern.match(line.strip())  # Strip whitespace and try to match the pattern
    if match:
        extension = match.group("extension").lstrip(".").lower()  # Remove leading dot, convert to lowercase
        description = match.group("description").strip()
        file_definitions[extension] = description

# Print the extracted dictionary
print(file_definitions)

# Optionally, save it as a JSON file
import json
with open("file_definitions.json", "w", encoding="utf-8") as f:
    json.dump(file_definitions, f, indent=4)

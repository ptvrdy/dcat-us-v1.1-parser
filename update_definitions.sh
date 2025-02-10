#!/bin/bash

# Navigate to the project directory
cd "C:\source\repos\dcat-us-v1.1-parser"

# Run the Python script to update file_definitions.json
python scrape.py

# Check if there are changes
if git diff --quiet file_definitions.json; then
    echo "No changes detected, skipping commit."
else
    # Stage, commit, and push if there are updates
    git add file_definitions.json
    git commit -m "Updated file definitions on $(date)"
    git push origin main  # Change "main" if your branch has a different name
    echo "File definitions updated and pushed!"
fi

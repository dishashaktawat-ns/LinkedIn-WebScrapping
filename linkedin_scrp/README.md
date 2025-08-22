# LinkedIn Data Extraction Pipeline

A robust pipeline for extracting professional profiles from LinkedIn company pages.

## Features
- Extracts profile data (name, position, connection level, etc.)
- Handles pagination automatically
- Cleans and normalizes data
- Saves results to Excel

## Commands
python main.py

## Data Model
The extracted data follows this schema:
```json
{
  "name": "string",
  "position": "string",
  "connection": "string",
  "location": "string",
  "profile_url": "string",
  "image_url": "string"
}


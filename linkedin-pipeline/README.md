# LinkedIn Data Pipeline with Firecrawl

This pipeline is designed to scrape LinkedIn company pages using Firecrawl, with robust data cleaning, validation, and enrichment capabilities.

##  Important Notice: LinkedIn Scraping Limitations

- LinkedIn scraping via Firecrawl requires special account permissions
- You'll need to contact Firecrawl support to enable LinkedIn scraping for your account
- Even with permissions, LinkedIn may block requests due to their strict anti-scraping measures
## A. Create a Firecrawl Account
 Go to Firecrawl's Signup Page

## B. Get Your API Key
Log in to your Firecrawl Dashboard
Navigate to API Keys in the sidebar
Click "Create New Key"
Copy the generated API key (store it securely)
## Features

- Scrapes company profiles, job postings, and associated members
- Handles data validation and cleaning
- Enriches data with metadata and derived fields
- Saves results to JSON files

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
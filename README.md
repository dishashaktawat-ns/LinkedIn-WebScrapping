# LinkedIn Company Scraper

This Python script logs into LinkedIn with your credentials and scrapes publicly available information from a company's LinkedIn page using **[linkedin-scraper](https://pypi.org/project/linkedin-scraper/)** and **Selenium**.

⚠️ **Disclaimer**:  
Scraping LinkedIn may violate their [Terms of Service](https://www.linkedin.com/legal/user-agreement). Use this script only for **educational purposes** or with explicit permission. Your account may be restricted or banned if LinkedIn detects automated scraping.

---

##  Features

- Logs into LinkedIn with your username & password.  
- Scrapes company details such as:
  - Company name
  - About section
  - Website
  - Phone
  - Headquarters
  - Founded year
  - Company type
  - Company size
  - Specialties
  - Affiliated companies  

---

## ⚙️ Requirements

Make sure you have the following installed:

- Python 3.8+
- Google Chrome browser
- Required Python packages:
  ```bash
  pip install selenium webdriver-manager linkedin-scraper
 Usage
Clone this repository or save the script file.

Replace your LinkedIn credentials in the script:

linkedin_email = "your_email@example.com"
linkedin_password = "your_password"
investec_url = "https://www.linkedin.com/company/investec/"
Run the script:


python linkedin_scraping.py
The script will:

Open Chrome

Log into LinkedIn

Navigate to the company page

Print scraped details in the console

Example Output
--- Scraped Company Information ---
Name: Investec
About: Investec is a specialist bank and asset manager...
Website: https://www.investec.com
Phone: +44 20 7597 4000
Headquarters: London, England
Founded: 1974
Company Type: Public Company
Company Size: 10,001+ employees
Specialties: Banking, Wealth Management, Asset Management
Affiliated Companies: Investec Australia, Investec South Africa
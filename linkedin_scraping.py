import os
import time
from linkedin_scraper import Company, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import traceback

def scrape_linkedin_company_with_login(company_url, email, password):
    """
    Scrapes a LinkedIn company page for publicly available information after logging in.

    Args:
        company_url (str): The URL of the LinkedIn company page to scrape.
        email (str): Your LinkedIn account email.
        password (str): Your LinkedIn account password.

    Returns:
        None
    """
    # --- Step 1: Set up the Chrome WebDriver ---
    # This setup is crucial for the scraper to work.
    # It automatically downloads and manages the correct ChromeDriver version.
    print("Setting up the Chrome WebDriver. This may take a moment...")
    try:
        # Configure Chrome options to run in headless mode (no browser window visible).
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Runs Chrome in the background
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the WebDriver with the options.
        # The ChromeDriverManager automatically handles the driver binary.
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("WebDriver setup successful. Attempting to log in...")
        
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        print("Please ensure you have Chrome installed and that your internet connection is stable.")
        return

    # --- Step 2: Log in to LinkedIn ---
    try:
        # Use the actions.login function from the library to handle the login process.
        actions.login(driver, email, password)
        print("Login successful.")

        # --- Step 3: Use the linkedin_scraper library to get company data ---
        # The library now has an active, logged-in session to work with.
        company = Company(linkedin_url=company_url, driver=driver,get_employees=False, close_on_complete=True)

        # Wait a moment for the scraping process to complete.
        time.sleep(20)

        # --- Step 4: Print the scraped information ---
        print("\n--- Scraped Company Information ---")
        print(f"Name: {company.name}")
        print(f"About: {company.about_us}")
        print(f"Website: {company.website}")
        print(f"Phone: {company.phone}")
        print(f"Headquarters: {company.headquarters}")
        print(f"Founded: {company.founded}")
        print(f"Company Type: {company.company_type}")
        print(f"Company Size: {company.company_size}")
        print(f"Specialties: {company.specialties}")
        print(f"Affiliated Companies: {', '.join(company.affiliated_companies)}")

    except Exception as e:
        print(traceback.format_exc())
        print(f"\nAn error occurred during scraping: {e}")
        print("This could be due to LinkedIn's anti-bot measures, changes to their website's HTML, a network issue, or incorrect login credentials.")
    
    finally:
        # Ensure the driver is closed even if an error occurs.
        if 'driver' in locals():
            driver.quit()

# --- Main execution block ---
if __name__ == "__main__":
    # IMPORTANT: Replace these with your actual LinkedIn credentials.
    # Be cautious when storing credentials directly in code.
    linkedin_email = "dishashaktawat67@gmail.com"
    linkedin_password = ""# Replace your linkedin password
    investec_url = "https://www.linkedin.com/company/investec/"
    
    scrape_linkedin_company_with_login(investec_url, linkedin_email, linkedin_password)

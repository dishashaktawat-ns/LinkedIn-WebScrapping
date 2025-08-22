
from config import Config
from extract.linkedin_extractor import LinkedInExtractor
from transform.data_cleaner import DataCleaner
from load.data_loader import DataLoader


def main():
    # Initialize components
    extractor = LinkedInExtractor()
    cleaner = DataCleaner()
    loader = DataLoader()

    # Extract data
    print(f"[+] Fetching profiles for {Config.COMPANY_SLUG}...")
    profiles = extractor.fetch_profiles(Config.START, Config.END, Config.STEP)

    if profiles:
        # Clean and transform data
        cleaned_profiles = cleaner.clean_profiles(profiles)
        df = cleaner.to_dataframe(cleaned_profiles)

        # Save data
        loader.save_to_excel(df)
    else:
        print("[!] No profiles extracted.")


if __name__ == "__main__":
    main()
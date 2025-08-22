import json
import time
import logging
from typing import List
from datetime import datetime
from pathlib import Path

from ingestion.scraper import LinkedInScraper
from transformation.cleaner import DataCleaner
from transformation.enricher import DataEnricher

logger = logging.getLogger(__name__)


class LinkedInPipeline:
    def __init__(self, firecrawl_api_key: str):
        self.scraper = LinkedInScraper(firecrawl_api_key)
        self.cleaner = DataCleaner()
        self.enricher = DataEnricher()

    def run(self, company_urls: List[str], output_dir: str = "outputs"):

        try:

            Path(output_dir).mkdir(exist_ok=True)

            logger.info("Starting LinkedIn scraping pipeline")


            logger.info(f"Scraping {len(company_urls)} company pages")
            raw_data = self.scraper.scrape_companies(company_urls)

            if not raw_data:
                logger.error("No data was scraped successfully")
                return False


            logger.info("Cleaning scraped data")
            cleaned_data = self.cleaner.clean_companies_data(raw_data)


            logger.info("Enriching cleaned data")
            enriched_data = self.enricher.enrich_companies_data(cleaned_data)


            output_path = Path(output_dir) / f"linkedin_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_path, 'w') as f:
                json.dump(enriched_data, f, indent=2)

            logger.info(f"Pipeline completed successfully. Output saved to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return False


def main():

    FIRE_CRAWL_API_KEY = "fc-96658a668b9248c7bf191d3bbfcfe6b0"
    COMPANY_URLS = [
        "https://www.linkedin.com/company/investec/",
        "https://www.linkedin.com/company/gf-holdings-hong-kong/",
        "https://www.linkedin.com/company/ebshk/"
    ]

    # Initialize and run pipeline
    pipeline = LinkedInPipeline(FIRE_CRAWL_API_KEY)
    success = pipeline.run(COMPANY_URLS)

    if not success:
        logger.error("Pipeline execution encountered errors")


if __name__ == "__main__":
    main()
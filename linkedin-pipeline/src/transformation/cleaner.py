import logging
from typing import List, Dict
from datetime import datetime
from ingestion.schemas import LinkedInCompany

logger = logging.getLogger(__name__)


class DataCleaner:
    @staticmethod
    def clean_company_data(raw_data: Dict) -> Dict:
        """
        Clean and validate raw company data
        Args:
            raw_data: Raw scraped data from LinkedIn
        Returns:
            Cleaned and validated data
        """
        try:
            # Validate against our schema
            validated = LinkedInCompany(**raw_data)

            # Additional cleaning
            cleaned_data = validated.dict()

            # Standardize location format
            if cleaned_data.get('location'):
                cleaned_data['location'] = cleaned_data['location'].split('·')[0].strip()

            return cleaned_data

        except Exception as e:
            logger.error(f"Data cleaning failed: {str(e)}")
            raise

    @staticmethod
    def clean_companies_data(raw_data: List[Dict]) -> List[Dict]:
        """Clean multiple company records"""
        cleaned_data = []
        for record in raw_data:
            try:
                cleaned = DataCleaner.clean_company_data(record)
                cleaned_data.append(cleaned)
            except Exception:
                continue
        return cleaned_data
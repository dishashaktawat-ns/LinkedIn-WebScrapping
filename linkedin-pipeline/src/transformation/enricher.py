import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class DataEnricher:
    @staticmethod
    def enrich_company_data(cleaned_data: Dict) -> Dict:
        """
        Add additional metadata and enrich the data
        Args:
            cleaned_data: Validated and cleaned company data
        Returns:
            Enriched company data
        """
        try:
            enriched = cleaned_data.copy()

            # Add timestamp
            enriched['extraction_timestamp'] = datetime.utcnow().isoformat()

            # Add metadata about the data quality
            enriched['metadata'] = {
                'has_description': bool(enriched.get('description')),
                'has_jobs': len(enriched.get('jobs', [])) > 0,
                'has_members': len(enriched.get('associated_members', [])) > 0,
                'jobs_count': len(enriched.get('jobs', [])),
                'members_count': len(enriched.get('associated_members', []))
            }

            # Add derived fields
            if enriched.get('follower_count'):
                enriched['follower_range'] = (
                    "1-10K" if enriched['follower_count'] < 10000 else
                    "10-50K" if enriched['follower_count'] < 50000 else
                    "50-100K" if enriched['follower_count'] < 100000 else
                    "100-500K" if enriched['follower_count'] < 500000 else
                    "500K+"
                )

            return enriched

        except Exception as e:
            logger.error(f"Data enrichment failed: {str(e)}")
            raise

    @staticmethod
    def enrich_companies_data(cleaned_data: List[Dict]) -> List[Dict]:
        """Enrich multiple company records"""
        enriched_data = []
        for record in cleaned_data:
            try:
                enriched = DataEnricher.enrich_company_data(record)
                enriched_data.append(enriched)
            except Exception:
                continue
        return enriched_data
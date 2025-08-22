# transform/data_cleaner.py
import pandas as pd
from typing import List, Dict


class DataCleaner:
    @staticmethod
    def clean_profiles(profiles: List[Dict]) -> List[Dict]:
        cleaned = []
        for profile in profiles:
            try:
                cleaned.append({
                    'name': profile.get('name', '').strip(),
                    'position': profile.get('position', '').strip(),
                    'connection': profile.get('connection', '').strip(),
                    'location': profile.get('location', '').strip(),
                    'profile_url': profile.get('profile_url', '').strip(),
                    'image_url': profile.get('image_url', '').strip()
                })
            except Exception as e:
                print(f"Error cleaning profile: {e}")
        return cleaned

    @staticmethod
    def to_dataframe(profiles: List[Dict]) -> pd.DataFrame:
        return pd.DataFrame(profiles)
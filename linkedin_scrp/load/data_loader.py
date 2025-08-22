# load/data_loader.py
import pandas as pd
from config import Config

class DataLoader:
    @staticmethod
    def save_to_excel(df: pd.DataFrame):
        try:
            filename = f"linkedin_profiles_{Config.COMPANY_SLUG}.xlsx"
            df.to_excel(filename, index=False)
            print(f"[+] Data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
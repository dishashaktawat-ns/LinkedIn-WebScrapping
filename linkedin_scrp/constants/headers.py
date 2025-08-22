# constants/headers.py
from config import Config

def get_headers():
    return {
        "User-Agent": Config.USER_AGENT,
        "Accept": "application/vnd.linkedin.normalized+json+2.1",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "csrf-token": Config.CSRF_TOKEN,
        "Priority": "u=1, i",
        "Referer": f"https://www.linkedin.com/company/{Config.COMPANY_SLUG}/people/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-li-lang": "en_US",
        "x-restli-protocol-version": "2.0.0",
        "cookie": Config.COOKIE
    }
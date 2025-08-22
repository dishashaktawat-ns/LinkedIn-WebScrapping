# # extract/linkedin_extractor.py
# import json
# import time
# import requests
# from urllib.parse import quote
# from typing import List, Dict, Optional
# from constants.api import APIConstants
# from constants.headers import get_headers
#
#
# class LinkedInExtractor:
#     def __init__(self):
#         self.headers = get_headers()
#
#     def _build_url(self, start: int) -> str:
#         variables = {
#             "start": start,
#             "origin": "FACETED_SEARCH",
#             "query": {
#                 "flagshipSearchIntent": "ORGANIZATIONS_PEOPLE_ALUMNI",
#                 "queryParameters": [
#                     {"key": "currentCompany", "value": [APIConstants.COMPANY_ID]},
#                     {"key": "resultType", "value": ["ORGANIZATION_ALUMNI"]}
#                 ],
#                 "includeFiltersInResponse": True
#             },
#             "count": 20
#         }
#         return f"{APIConstants.BASE_URL}?variables={quote(json.dumps(variables))}&queryId={APIConstants.QUERY_ID}"
#
#     def _extract_profile(self, entity_result: Dict) -> Optional[Dict]:
#         if not isinstance(entity_result, dict):
#             return None
#
#         # Extract connection level
#         badge_text = entity_result.get('badgeText', {})
#         connection = badge_text.get('text', '').replace('•', '').strip() if isinstance(badge_text, dict) else ''
#
#         profile = {
#             'name': entity_result.get('title', {}).get('text', 'N/A'),
#             'position': entity_result.get('primarySubtitle', {}).get('text', 'N/A'),
#             'connection': connection,
#             'location': entity_result.get('secondarySubtitle', {}).get('text', ''),
#             'profile_url': entity_result.get('navigationUrl', ''),
#             'image_url': self._extract_profile_image(
#             entity_result.get('image', {}))
#         }
#         return profile
#
#     def _extract_profile_image(self, image_data: Dict) -> str:
#         if not isinstance(image_data, dict) or 'attributes' not in image_data:
#             return ''
#
#         for attr in image_data['attributes']:
#             detail_data = attr.get('detailData', {})
#             if 'nonEntityProfilePicture' in detail_data:
#                 vector_image = detail_data['nonEntityProfilePicture'].get('vectorImage', {})
#                 if isinstance(vector_image, dict) and 'artifacts' in vector_image:
#                     for artifact in vector_image['artifacts']:
#                         if isinstance(artifact, dict) and artifact.get('width') == 100:
#                             root_url = vector_image.get('rootUrl', '')
#                             path = artifact.get('fileIdentifyingUrlPathSegment', '')
#                             return f"{root_url}{path}" if root_url else path
#         return ''
#
#     def extract_profiles(self, data: Dict) -> List[Dict]:
#         profiles = []
#         try:
#             clusters = data.get('data', {}).get('searchDashClustersByAll', {})
#             for element in clusters.get('elements', []):
#                 for item in element.get('items', []):
#                     entity_result = item.get('item', {}).get('entityResult')
#                     profile = self._extract_profile(entity_result)
#                     if profile:
#                         profiles.append(profile)
#         except Exception as e:
#             print(f"Error extracting profiles: {e}")
#         return profiles
#
#     def fetch_profiles(self, start: int, end: int, step: int) -> List[Dict]:
#         profiles = []
#         for num in range(start, end, step):
#             try:
#                 url = self._build_url(num)
#                 response = requests.get(url, headers=self.headers, timeout=10)
#                 response.raise_for_status()
#
#                 data = response.json()
#                 batch = self.extract_profiles(data)
#                 profiles.extend(batch)
#                 print(f"[+] Extracted {len(batch)} profiles starting from index {num}.")
#                 time.sleep(10)  # Respect rate limits
#             except requests.HTTPError as e:
#                 print(f"HTTP Error fetching profiles at index {num}: {e.response.status_code}")
#             except Exception as e:
#                 print(f"Error fetching profiles at index {num}: {e}")
#         return profiles


# extract/linkedin_extractor.py
import json
import time
import requests
from urllib.parse import quote
from typing import List, Dict, Optional
from constants.api import APIConstants
from constants.headers import get_headers


class LinkedInExtractor:
    def __init__(self):
        self.headers = get_headers()
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _build_url(self, start: int) -> str:
        """Build the GraphQL URL with proper parameter encoding"""
        variables = {
            "start": start,
            "origin": "FACETED_SEARCH",
            "query": {
                "flagshipSearchIntent": "ORGANIZATIONS_PEOPLE_ALUMNI",
                "queryParameters": [
                    {"key": "currentCompany", "value": [APIConstants.COMPANY_ID]},
                    {"key": "resultType", "value": ["ORGANIZATION_ALUMNI"]}
                ],
                "includeFiltersInResponse": True
            },
            "count": 20
        }

        # Encode variables exactly as LinkedIn expects
        encoded_vars = quote(json.dumps(variables))
        return f"{APIConstants.BASE_URL}?variables={encoded_vars}&queryId={APIConstants.QUERY_ID}"

    def _extract_profile(self, entity_result: Dict) -> Optional[Dict]:
        """Extract profile data from API response"""
        if not isinstance(entity_result, dict):
            return None

        # Extract connection level
        badge_text = entity_result.get('badgeText', {})
        connection = badge_text.get('text', '').replace('•', '').strip() if isinstance(badge_text, dict) else ''

        profile = {
            'name': entity_result.get('title', {}).get('text', 'N/A'),
            'position': entity_result.get('primarySubtitle', {}).get('text', 'N/A'),
            'connection': connection,
            'location': entity_result.get('secondarySubtitle', {}).get('text', ''),
            'profile_url': entity_result.get('navigationUrl', ''),
            'image_url': self._extract_profile_image(entity_result.get('image', {}))
        }
        return profile

    def _extract_profile_image(self, image_data: Dict) -> str:
        """Extract profile image URL if available"""
        if not isinstance(image_data, dict) or 'attributes' not in image_data:
            return ''

        for attr in image_data['attributes']:
            if not isinstance(attr, dict):
                continue

            detail_data = attr.get('detailData', {})
            if 'nonEntityProfilePicture' in detail_data:
                vector_image = detail_data['nonEntityProfilePicture'].get('vectorImage', {})
                if isinstance(vector_image, dict) and 'artifacts' in vector_image:
                    for artifact in vector_image['artifacts']:
                        if isinstance(artifact, dict) and artifact.get('width') == 100:
                            root_url = vector_image.get('rootUrl', '')
                            path = artifact.get('fileIdentifyingUrlPathSegment', '')
                            return f"{root_url}{path}" if root_url else path
        return ''

    def _validate_response(self, response: requests.Response) -> bool:
        """Validate the API response"""
        if response.status_code != 200:
            print(f"Request failed with status {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response content (first 500 chars): {response.text[:500]}")
            return False

        try:
            data = response.json()
            if 'data' not in data:
                print("Response missing 'data' field")
                return False
            return True
        except json.JSONDecodeError:
            print("Invalid JSON response")
            return False

    def extract_profiles(self, data: Dict) -> List[Dict]:
        """Extract profiles from API response data"""
        profiles = []
        try:
            clusters = data.get('data', {}).get('searchDashClustersByAll', {})
            elements = clusters.get('elements', [])

            for element in elements:
                items = element.get('items', [])
                for item in items:
                    if not isinstance(item, dict):
                        continue

                    entity_result = item.get('item', {}).get('entityResult')
                    profile = self._extract_profile(entity_result)
                    if profile:
                        profiles.append(profile)

        except Exception as e:
            print(f"Error extracting profiles: {str(e)}")

        return profiles

    def fetch_profiles(self, start: int, end: int, step: int) -> List[Dict]:
        """Fetch profiles from LinkedIn API with pagination"""
        profiles = []

        for num in range(start, end, step):
            try:
                url = self._build_url(num)
                print(f"\n[+] Fetching profiles starting from index {num}")
                print(f"Request URL: {url[:150]}...")  # Show partial URL for debugging

                response = self.session.get(url, timeout=15)

                if not self._validate_response(response):
                    continue

                data = response.json()
                batch = self.extract_profiles(data)

                if not batch:
                    print(f"No profiles found in batch {num}")
                    continue

                profiles.extend(batch)
                print(f"Extracted {len(batch)} profiles")

                # Respect rate limits
                time.sleep(10)

            except requests.RequestException as e:
                print(f"Request failed: {str(e)}")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")

        return profiles






# extract/linkedin_extractor.py
# import json
# import time
# import requests
# from urllib.parse import quote
# from typing import List, Dict, Optional
# from constants.api import APIConstants
# from constants.headers import get_headers
#
#
# class LinkedInExtractor:
#     def __init__(self):
#         self.headers = get_headers()
#
#     def _build_url(self, start: int) -> str:
#         # Use the exact format that works in your manual test
#         variables = {
#             "start": start,
#             "origin": "FACETED_SEARCH",
#             "query": {
#                 "flagshipSearchIntent": "ORGANIZATIONS_PEOPLE_ALUMNI",
#                 "queryParameters": [
#                     {"key": "currentCompany", "value": [APIConstants.COMPANY_ID]},
#                     {"key": "resultType", "value": ["ORGANIZATION_ALUMNI"]}
#                 ],
#                 "includeFiltersInResponse": True
#             },
#             "count": 20
#         }
#
#         # Convert to the format that matches your working URL
#         params = f"(start:{start},origin:FACETED_SEARCH,query:(flagshipSearchIntent:ORGANIZATIONS_PEOPLE_ALUMNI,queryParameters:List((key:currentCompany,value:List({APIConstants.COMPANY_ID})),(key:resultType,value:List(ORGANIZATION_ALUMNI))),includeFiltersInResponse:true),count:20)"
#
#         return f"{APIConstants.BASE_URL}?variables={quote(params)}&queryId={APIConstants.QUERY_ID}"
#
#     def _extract_profile(self, entity_result: Dict) -> Optional[Dict]:
#         if not isinstance(entity_result, dict):
#             return None
#
#         # Extract connection level
#         badge_text = entity_result.get('badgeText', {})
#         connection = badge_text.get('text', '').replace('•', '').strip() if isinstance(badge_text, dict) else ''
#
#         profile = {
#             'name': entity_result.get('title', {}).get('text', 'N/A'),
#             'position': entity_result.get('primarySubtitle', {}).get('text', 'N/A'),
#             'connection': connection,
#             'location': entity_result.get('secondarySubtitle', {}).get('text', ''),
#             'profile_url': entity_result.get('navigationUrl', ''),
#             'image_url': self._extract_profile_image(entity_result.get('image', {}))
#         }
#         return profile
#
#     def _extract_profile_image(self, image_data: Dict) -> str:
#         if not isinstance(image_data, dict) or 'attributes' not in image_data:
#             return ''
#
#         for attr in image_data['attributes']:
#             detail_data = attr.get('detailData', {})
#             if 'nonEntityProfilePicture' in detail_data:
#                 vector_image = detail_data['nonEntityProfilePicture'].get('vectorImage', {})
#                 if isinstance(vector_image, dict) and 'artifacts' in vector_image:
#                     for artifact in vector_image['artifacts']:
#                         if isinstance(artifact, dict) and artifact.get('width') == 100:
#                             root_url = vector_image.get('rootUrl', '')
#                             path = artifact.get('fileIdentifyingUrlPathSegment', '')
#                             return f"{root_url}{path}" if root_url else path
#         return ''
#
#     def extract_profiles(self, data: Dict) -> List[Dict]:
#         profiles = []
#         try:
#             clusters = data.get('data', {}).get('searchDashClustersByAll', {})
#             for element in clusters.get('elements', []):
#                 for item in element.get('items', []):
#                     entity_result = item.get('item', {}).get('entityResult')
#                     profile = self._extract_profile(entity_result)
#                     if profile:
#                         profiles.append(profile)
#         except Exception as e:
#             print(f"Error extracting profiles: {e}")
#         return profiles
#
#     def fetch_profiles(self, start: int, end: int, step: int) -> List[Dict]:
#         profiles = []
#         for num in range(start, end, step):
#             try:
#                 url = self._build_url(num)
#                 print(f"DEBUG - Request URL: {url}")  # Add debug logging
#                 response = requests.get(url, headers=self.headers, timeout=10)
#
#                 # Add more detailed error information
#                 if response.status_code != 200:
#                     print(f"DEBUG - Response Headers: {response.headers}")
#                     print(f"DEBUG - Response Content: {response.text[:500]}...")
#
#                 response.raise_for_status()
#
#                 data = response.json()
#                 batch = self.extract_profiles(data)
#                 profiles.extend(batch)
#                 print(f"[+] Extracted {len(batch)} profiles starting from index {num}.")
#                 time.sleep(10)  # Respect rate limits
#             except requests.HTTPError as e:
#                 print(f"HTTP Error fetching profiles at index {num}: {e.response.status_code}")
#                 print(f"Error details: {e.response.text[:500]}...")
#             except Exception as e:
#                 print(f"Error fetching profiles at index {num}: {str(e)}")
#         return profiles
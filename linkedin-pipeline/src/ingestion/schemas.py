from pydantic import BaseModel, validator
from typing import List, Optional
import re


class LinkedInJob(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    posted_date: Optional[str] = None
    link: Optional[str] = None


class LinkedInMember(BaseModel):
    name: str
    position: Optional[str] = None
    duration: Optional[str] = None
    connection_level: Optional[str] = None


class LinkedInCompany(BaseModel):
    company_name: str
    description: Optional[str] = None
    follower_count: Optional[int] = None
    employee_count: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    jobs: List[LinkedInJob] = []
    associated_members: List[LinkedInMember] = []

    @validator('follower_count', pre=True)
    def parse_follower_count(cls, v):
        if not v:
            return None
        if isinstance(v, int):
            return v
        try:
            # Handle formats like "542K followers" or "1.2M followers"
            v = v.lower().replace('followers', '').strip()
            if 'k' in v:
                return int(float(v.replace('k', '')) * 1000)
            if 'm' in v:
                return int(float(v.replace('m', '')) * 1000000)
            return int(v.replace(',', ''))
        except (ValueError, AttributeError):
            return None

    @validator('employee_count', pre=True)
    def clean_employee_count(cls, v):
        if not v:
            return None
        # Handle formats like "5K-10K employees" or "10,001+ employees"
        return v.replace('employees', '').strip()
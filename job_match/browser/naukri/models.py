from pydantic import BaseModel


class CuratedJobDetails(BaseModel):
    company: str
    title: str
    location: str
    salary: str
    skills: str
    experience: str
from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    name: str
    skills: list[str] = Field(default_factory=list)
    years_experience: float | None = None
    preferred_locations: list[str] = Field(default_factory=list)
    target_titles: list[str] = Field(default_factory=list)
    resume_text: str = ""


class JobMatchResult(BaseModel):
    company: str
    title: str
    score: float = Field(ge=0, le=100)
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    skill_score: float = Field(ge=0, le=60)
    title_score: float = Field(ge=0, le=20)
    location_score: float = Field(ge=0, le=10)
    experience_score: float = Field(ge=0, le=10)
    recommendation: str
from __future__ import annotations

import re

from job_match.browser.naukri.models import CuratedJobDetails
from job_match.matching.models import CandidateProfile, JobMatchResult


class DeterministicMatchEngine:
    def calculate(
        self,
        job: CuratedJobDetails,
        candidate: CandidateProfile,
    ) -> JobMatchResult:
        job_skills = self._split_skills(job.skills)
        candidate_skills = {
            self._normalize(skill)
            for skill in candidate.skills
        }
        matched_skills = [
            skill
            for skill in job_skills
            if self._normalize(skill) in candidate_skills
        ]
        missing_skills = [
            skill for skill in job_skills if skill not in matched_skills
        ]

        skill_score = self._score_skills(
            len(matched_skills),
            len(job_skills),
        )
        title_score = self._score_title(job.title, candidate.target_titles)
        location_score = self._score_location(
            job.location,
            candidate.preferred_locations,
        )
        experience_score = self._score_experience(
            job.experience,
            candidate.years_experience,
        )
        total_score = round(
            skill_score + title_score + location_score + experience_score,
            2,
        )

        return JobMatchResult(
            company=job.company,
            title=job.title,
            score=total_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            skill_score=skill_score,
            title_score=title_score,
            location_score=location_score,
            experience_score=experience_score,
            recommendation="fit" if total_score >= 70 else "not_fit",
        )

    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"[^a-z0-9+#.]", "", value.lower())

    @classmethod
    def _split_skills(cls, skills: str) -> list[str]:
        return [
            skill.strip()
            for skill in skills.split(",")
            if cls._normalize(skill)
        ]

    @staticmethod
    def _score_skills(matched_count: int, total_count: int) -> float:
        if not total_count:
            return 0
        return round((matched_count / total_count) * 60, 2)

    @classmethod
    def _score_title(cls, job_title: str, target_titles: list[str]) -> float:
        normalized_job_title = cls._normalize(job_title)
        return 20 if any(
            cls._normalize(title) in normalized_job_title
            or normalized_job_title in cls._normalize(title)
            for title in target_titles
        ) else 0

    @classmethod
    def _score_location(
        cls,
        job_location: str,
        preferred_locations: list[str],
    ) -> float:
        if not preferred_locations:
            return 0
        normalized_job_location = cls._normalize(job_location)
        return 10 if any(
            cls._normalize(location) in normalized_job_location
            for location in preferred_locations
        ) else 0

    @staticmethod
    def _score_experience(
        job_experience: str,
        candidate_years: float | None,
    ) -> float:
        if candidate_years is None:
            return 0
        match = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", job_experience)
        if not match:
            return 0
        minimum_years = float(match.group(1))
        return 10 if candidate_years >= minimum_years else 0
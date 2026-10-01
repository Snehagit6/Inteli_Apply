from __future__ import annotations

import re
from pathlib import Path

from docx import Document

from job_match.matching.models import CandidateProfile


class ResumeProfileParser:
    @classmethod
    def from_docx(cls, resume_path: str | Path) -> CandidateProfile:
        paragraphs = [
            paragraph.text.strip()
            for paragraph in Document(resume_path).paragraphs
            if paragraph.text.strip()
        ]
        resume_text = "\n".join(paragraphs)

        return CandidateProfile(
            name=cls._value_after_label(paragraphs, "Name") or "Unknown",
            skills=cls._extract_skills(paragraphs),
            years_experience=cls._extract_years(resume_text),
            preferred_locations=cls._extract_locations(paragraphs),
            target_titles=cls._extract_titles(resume_text),
            resume_text=resume_text,
        )

    @staticmethod
    def _value_after_label(paragraphs: list[str], label: str) -> str | None:
        prefix = f"{label}:"
        for paragraph in paragraphs:
            if paragraph.lower().startswith(prefix.lower()):
                return paragraph[len(prefix):].strip()
        return None

    @classmethod
    def _extract_skills(cls, paragraphs: list[str]) -> list[str]:
        try:
            start = next(
                index
                for index, paragraph in enumerate(paragraphs)
                if paragraph.upper() == "SKILLSET"
            )
        except StopIteration:
            return []

        skills = []
        for paragraph in paragraphs[start + 1:]:
            if paragraph.upper() == "PROFESSIONAL HIGHLIGHTS":
                break
            skills.extend(
                skill.strip(" •")
                for skill in paragraph.split(",")
                if skill.strip(" •")
            )
        return skills

    @staticmethod
    def _extract_years(resume_text: str) -> float | None:
        match = re.search(r"(\d+(?:\.\d+)?)\+?\s+years? of experience", resume_text, re.IGNORECASE)
        return float(match.group(1)) if match else None

    @classmethod
    def _extract_locations(cls, paragraphs: list[str]) -> list[str]:
        location = cls._value_after_label(paragraphs, "Location")
        return [location] if location else []

    @staticmethod
    def _extract_titles(resume_text: str) -> list[str]:
        summary_match = re.search(
            r"PROFESSIONAL SUMMARY\s+(.+?)\s+with\s+\d+(?:\.\d+)?\+?\s+years?",
            resume_text,
            re.IGNORECASE,
        )
        if not summary_match:
            return []
        return [
            title.strip()
            for title in summary_match.group(1).split("/")
            if title.strip()
        ]
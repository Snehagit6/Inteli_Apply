import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_match.matching import ResumeProfileParser


def test_resume_parser_builds_candidate_profile():
    resume_path = Path(__file__).parents[1] / "resumes" / "RESUME_2026.docx"

    profile = ResumeProfileParser.from_docx(resume_path)

    print(profile.name)
    print(profile.years_experience)
    print(profile.preferred_locations)
    print(profile.skills)
    print(profile.target_titles)
    print(profile.resume_text)

    assert profile.name == "Sneha Mazumder"
    assert profile.years_experience == 10
    assert profile.preferred_locations == ["Bangalore"]
    assert "Python" in profile.skills
    assert "Senior SDET" in profile.target_titles
    assert profile.resume_text
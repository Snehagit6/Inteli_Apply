import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_match.browser.naukri.models import CuratedJobDetails
from job_match.matching import CandidateProfile, DeterministicMatchEngine


def test_match_engine_returns_transparent_score():
    job = CuratedJobDetails(
        company="Example Corp",
        title="Senior Python SDET",
        location="Bengaluru",
        salary="₹25L - ₹40L/year",
        skills="Python, Playwright, Selenium",
        experience="5-10 Yrs",
    )
    candidate = CandidateProfile(
        name="Sneha",
        skills=["Python", "Playwright", "Selenium"],
        years_experience=8,
        preferred_locations=["Bengaluru"],
        target_titles=["SDET"],
    )

    result = DeterministicMatchEngine().calculate(job, candidate)

    assert result.score == 100
    assert result.matched_skills == ["Python", "Playwright", "Selenium"]
    assert result.missing_skills == []
    assert result.recommendation == "fit"


def test_match_engine_rejects_low_skill_match():
    job = CuratedJobDetails(
        company="Example Corp",
        title="Machine Learning Engineer",
        location="Bengaluru",
        salary="Not Disclosed",
        skills="Python, TensorFlow, Kubernetes",
        experience="5-10 Yrs",
    )
    candidate = CandidateProfile(
        name="Sneha",
        skills=["Python"],
        years_experience=2,
        preferred_locations=["Delhi"],
        target_titles=["QA Engineer"],
    )

    result = DeterministicMatchEngine().calculate(job, candidate)

    assert result.score < 70
    assert result.missing_skills == ["TensorFlow", "Kubernetes"]
    assert result.recommendation == "not_fit"
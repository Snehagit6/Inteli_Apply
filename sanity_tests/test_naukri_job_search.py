
import os
import time
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import expect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from job_match.browser.naukri.login import NaukriLoginPage
from job_match.browser.naukri.home_page import NaukriHomePage


load_dotenv()  # Load environment variables from .env file

email_id, pwd = os.getenv("NAUKRI_EMAIL"), os.getenv("NAUKRI_PASSWORD")
SCREENSHOT_PATH = Path(__file__).resolve().parents[1] / "ui_screen" / "naukri_job_search.png"

def test_job_search(naukri_login_page):
    logger.info("Step: Start headed Chromium browser")
    if not email_id or not pwd:
        pytest.fail("Set NAUKRI_EMAIL and NAUKRI_PASSWORD in .env before running this test")

    home_page = naukri_login_page.login_as(email_id, pwd)

    logger.info('Step: Validate page title is "Naukri TopTier"')
    expect(home_page.page).to_have_title("Naukri TopTier")
    jobs = home_page.view_curated_link().get_curated_job_details()
    assert jobs, "Expected at least one curated job"
    assert all(job.location and job.salary and job.skills and job.experience for job in jobs)
    logger.info(f"Collected {len(jobs)} curated jobs\n Job Details: {jobs}")
    SCREENSHOT_PATH.parent.mkdir(exist_ok=True)
    naukri_login_page.page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
    
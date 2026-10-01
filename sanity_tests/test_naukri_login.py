
import os
import sys
import pytest
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_match.browser.naukri.login import NaukriLoginPage

load_dotenv()  # Load environment variables from .env file

email_id, pwd = os.getenv("NAUKRI_EMAIL"), os.getenv("NAUKRI_PASSWORD")

def test_naukri_login():
    if not email_id or not pwd:
        pytest.fail("Set NAUKRI_EMAIL and NAUKRI_PASSWORD in .env before running this test")

    naukri_login = NaukriLoginPage()
    home_page = naukri_login.login_as(email_id, pwd)
    home_page.open_search()

import os
import sys
import logging
from pathlib import Path

import pytest
from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import Page

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_match.browser.naukri.login import NaukriLoginPage
from utilities.mail import send_email_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def pytest_configure(config):
    (PROJECT_ROOT / "reports").mkdir(exist_ok=True)


@pytest.fixture(autouse=True)
def loguru_to_pytest(caplog):
    caplog.set_level(logging.INFO)
    handler_id = logger.add(
        caplog.handler,
        format="{time:YYYY-MM-DD HH:mm:ss} [{level}] {name}: {message}",
        level="INFO",
    )
    yield
    logger.remove(handler_id)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"args": ["--start-maximized"]}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": None}

# def pytest_unconfigure(config):
#     send_email_report(
#         report_path=PROJECT_ROOT / "reports" / "pytest-report.html",
#         screenshot_path=PROJECT_ROOT / "ui_screen" / "naukri_job_search.png",
#     )


@pytest.fixture
def naukri_login_page(page: Page) -> NaukriLoginPage:
    return NaukriLoginPage(page)

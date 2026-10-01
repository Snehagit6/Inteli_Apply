import os, sys
from typing import Final

from loguru import logger
from playwright.sync_api import expect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_match.browser.base_page import BasePage
from job_match.browser.naukri.home_page import NaukriHomePage


class NaukriLoginPage(BasePage):
    URL: Final[str] = "https://www.naukri.com/"

    def open(self) -> "NaukriLoginPage":
        logger.info("Step: Open Naukri home page")
        self.page.goto(self.URL)
        return self

    def click_login(self) -> "NaukriLoginPage":
        logger.info("Step: Click Login link")
        login_link = self.page.locator("xpath=//a[@title='Jobseeker Login']")
        login_link.wait_for()
        login_link.click()
        return self

    def login(self, username: str, password: str) -> "NaukriLoginPage":
        logger.info("Step: Enter credentials and submit login form")
        self.page.get_by_placeholder("Enter your active Email ID / Username").fill(username)
        self.page.get_by_placeholder("Enter your password").fill(password)
        self.page.locator("xpath=//button[@type='submit']").click()
        return self

    def wait_for_dashboard(self):
        logger.info("Step: Create Naukri home page object")
        return NaukriHomePage(self.page)

    def login_as(self, username: str, password: str):
        self.open().click_login().login(username, password)
        return self.wait_for_dashboard()


# Example usage:
# naukri_login = NaukriLoginPage()
# home_page = naukri_login.login_as("your_email@example.com", "your_password")
# home_page.open_search()

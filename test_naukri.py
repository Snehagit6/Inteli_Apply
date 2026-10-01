import time
import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://www.naukri.com/")
    page.set_viewport_size({"width": 1920, "height": 1080})
    login_obj = page.get_by_role("link", name="Login")
    login_obj.wait_for()

    print(f"Title of webpage: {page.title()}")  # Get the title of the page
    login_obj.click()

    page.get_by_placeholder("Enter your active Email ID / Username").fill("snehatech611@gmail.com")
    page.get_by_placeholder("Enter your password").fill("Naukripass6!")
    page.locator("xpath=//button[@type='submit']").click()

    search_button = page.locator("xpath=//button[@aria-label='Search jobs here...']")
    expect(search_button).to_be_visible(timeout=10000)  # Wait for the search button to be visible

    # Alternative path
    # page.locator("xpath=//button[@class='google']").click()

import re
from loguru import logger
from playwright.sync_api import expect

from job_match.browser.base_page import BasePage
from job_match.browser.naukri.models import CuratedJobDetails


class NaukriHomePage(BasePage):

    def view_curated_link(self):
        logger.info("Step: Click on 'View all' for curated opportunities")
        curated_jobs_link = self.page.locator(
            "xpath=//h2[normalize-space()='Curated opportunities for you']"
            "/../../..//a[normalize-space()='View all']"
        )
        expect(curated_jobs_link).to_be_visible(timeout=10000)
        curated_jobs_link.click()
        return self

    def get_curated_job_details(self) -> list[CuratedJobDetails]:
        logger.info("Step: Get all curated jobs")
        expect(
            self.page.get_by_text("Opportunities for you", exact=True)
        ).to_be_visible(timeout=10000)

        job_cards = self.page.locator(
            "xpath=//img[@alt='Job']"
            "/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' cursor-pointer ')][1]"
        )
        expect(job_cards.first).to_be_visible(timeout=10000)

        previous_count = 0
        stable_rounds = 0
        for _ in range(60):
            current_count = job_cards.count()
            if current_count == previous_count:
                stable_rounds += 1
            else:
                stable_rounds = 0
                previous_count = current_count

            if stable_rounds >= 3:
                break

            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(750)

        jobs = []
        for index in range(job_cards.count()):
            card = job_cards.nth(index)
            jobs.append(
                CuratedJobDetails(
                    company=card.locator("xpath=.//h4").inner_text().strip(),
                    title=card.locator(
                        "xpath=.//ul/preceding-sibling::div[1]"
                    ).inner_text().strip(),
                    location=card.locator(
                        "xpath=.//li[.//img[@alt='location']]"
                    ).inner_text().strip(),
                    salary=card.locator(
                        "xpath=.//li[.//img[@alt='salary']]"
                    ).inner_text().strip(),
                    skills=card.locator(
                        "xpath=.//li[.//img[@alt='skills']]"
                    ).inner_text().strip(),
                    experience=card.locator(
                        "xpath=.//li[.//img[@alt='experience']]"
                    ).inner_text().strip(),
                )
            )

        return jobs

    def enter_search_inputs(self, search_input: str, location: str):
        logger.info("Step: Enter job search inputs")
        search_field = self.page.get_by_placeholder("Enter skills, designations, companies...")
        expect(search_field).to_be_visible(timeout=10000)
        search_field.fill(search_input)

        location_input = self.page.get_by_placeholder("Enter location")
        expect(location_input).to_be_visible(timeout=10000)
        location_input.fill(location)
        self.page.get_by_role("button", name=re.compile("Search jobs", re.IGNORECASE)).click()


    def wait_for_search_button(self):
        logger.info("Step: Wait for search button")
        search_button = self.page.locator("xpath=//button[@aria-label='Search jobs here...']")
        expect(search_button).to_be_visible(timeout=10000)
        return search_button

    def open_search(self):
        logger.info("Step: Submit job search")
        search_button = self.wait_for_search_button()
        search_button.click()
        return self


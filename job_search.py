import os
from typing import List
from time import sleep
import urllib.parse

from objects import Scraper
# from  import constants as c
from jobs import Job
# import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# from bs4 import BeautifulSoup

class JobSearch(Scraper):
    AREAS = ["recommended_jobs", None, "still_hiring", "more_jobs"]


    def __init__(self, driver, base_url="https://www.linkedin.com/jobs/", close_on_complete=False, scrape=True, scrape_recommended_jobs=True):
        super().__init__()
        self.driver = driver
        self.base_url = base_url


        if scrape:
            self.scrape(close_on_complete, scrape_recommended_jobs)


    def scrape(self, close_on_complete=True, scrape_recommended_jobs=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete, scrape_recommended_jobs=scrape_recommended_jobs)
        else:
            raise NotImplemented("This part is not implemented yet")


    def scrape_job_card(self, base_element) -> Job:
        job_div = self.wait_for_element_to_load(name="job-card-list__title", base=base_element)
        job_title = job_div.text.strip()
        linkedin_url = job_div.get_attribute("href")
        try:
            company = base_element.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle").text
        except Exception as e:
            company = None
        try:
            number_of_applicants = base_element.find_element(By.XPATH, "//*[@id=\"main\"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/div/span[5]").text
        except Exception as e:
            number_of_applicants = None
        try:
            post_date = base_element.find_element(By.XPATH, "//*[@id=\"main\"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/div/span[3]").text
        except Exception as e:
            post_date = None
        job_description = None


        job_description_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-description-content__text"))
        )

        # Once the element is found, extract its text
        job_description = job_description_element.text

        location = base_element.find_element(By.CLASS_NAME, "job-card-container__metadata-wrapper").text
        job = Job(linkedin_url=linkedin_url, job_title=job_title, company=company,posted_date=post_date,applicant_count=number_of_applicants,job_description=job_description, location=location, scrape=False, driver=self.driver)
        return job


    def scrape_logged_in(self, close_on_complete=True, scrape_recommended_jobs=True):
        driver = self.driver
        driver.get(self.base_url)
        if scrape_recommended_jobs:
            self.focus()
            sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)
            job_area = self.wait_for_element_to_load(name="scaffold-finite-scroll__content")
            areas = self.wait_for_all_elements_to_load(name="artdeco-card", base=job_area)
            for i, area in enumerate(areas):
                area_name = self.AREAS[i]
                if not area_name:
                    continue
                area_results = []
                for job_posting in area.find_elements_by_class_name("jobs-job-board-list__item"):
                    job = self.scrape_job_card(job_posting)
                    area_results.append(job)
                setattr(self, area_name, area_results)
        return


    def search(self, search_term: str) -> List[Job]:
        url = os.path.join(self.base_url, "search") + f"?keywords={urllib.parse.quote(search_term)}&refresh=true"
        self.driver.get(url)
        self.scroll_to_bottom()
        self.focus()
        # sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)

        job_listing_class_name = "jobs-search-results-list"
        job_listing = self.wait_for_element_to_load(name=job_listing_class_name)

        # self.scroll_class_name_element_to_page_percent(job_listing_class_name, 0.3)
        # self.focus()
        # sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)
        #
        # self.scroll_class_name_element_to_page_percent(job_listing_class_name, 0.6)
        # self.focus()
        # sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)
        #
        # self.scroll_class_name_element_to_page_percent(job_listing_class_name, 1)
        # self.focus()
        # sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)

        def wait_for_element(xpath):
            return WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )


        job_results = []
        for page_number in range(2, 101):
            try:
                number_of_results_xpath ="//*[@id=\"main\"]/div/div[2]/div[1]/header/div[1]/small/div"
                tempo = self.driver.find_elements(By.XPATH, number_of_results_xpath)
                xpath = f".//button[@aria-label='Page {page_number}']"
                if self.driver.find_elements(By.XPATH, xpath):
                    button = wait_for_element(xpath)
                    button.click()

                    self.scroll_class_name_element_to_page_percent(job_listing_class_name, 0.3)
                    self.focus()
                    sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)

                    self.scroll_class_name_element_to_page_percent(job_listing_class_name, 0.6)
                    self.focus()
                    sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)

                    self.scroll_class_name_element_to_page_percent(job_listing_class_name, 1)
                    self.focus()
                    sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)




                    job_cards = self.wait_for_all_elements_to_load(name="job-card-list", base=job_listing)
                    # job_cards.scr
                    for job_card in job_cards:
                        job_card.click()
                        # self.wait_for_all_elements_to_load(name="job-card-list", base=job_listing)
                        job = self.scrape_job_card(job_card)
                        job_results.append(job)
                        # sleep(1)

            except Exception as e:
                break


        return job_results



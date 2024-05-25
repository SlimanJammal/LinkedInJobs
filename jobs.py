from selenium.common.exceptions import TimeoutException

from objects import Scraper
import constants as c
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Job(Scraper):
    """
      Represents a job listing scraped from LinkedIn.

      Attributes:
          linkedin_url (str): The URL of the job listing on LinkedIn.
          job_title (str): The title of the job.
          driver: The Selenium WebDriver instance.
          company (str): The name of the company offering the job.
          company_linkedin_url (str): The LinkedIn URL of the company.
          location (str): The location of the job.
          full_time (str): The employment type (Full Time/Part Time).
          experience_years (str): The required years of experience.
          type (str): The type of education required (e.g., BSc, MSc, etc.).
          required_skills (str): Skills required for the job.
          needs_experience (str): Whether the job requires previous experience (Yes/No).
          posted_date (str): The date when the job was posted.
          applicant_count (int): The number of applicants for the job.
          job_description (str): The description of the job.
          benefits (str): The benefits associated with the job.
          salary: job's estimated monthly salary in location of the job

      Methods:
          scrape: Scrapes job details from LinkedIn.
          to_dict: Converts the job object into a dictionary.
      """
    def __init__(
        self,
        linkedin_url=None,
        job_title=None,
        company=None,
        company_linkedin_url="empty",
        location=None,
        posted_date=None,
        applicant_count=None,
        job_description=None,
        full_time=None,
        experience_years=None,
        type=None,
        required_skills=None,
        needs_experience=None,
        salary=None,
        benefits="empty",
        driver=None,
        close_on_complete=True,
        scrape=True,
    ):
        super().__init__()
        self.linkedin_url = linkedin_url
        self.job_title = job_title
        self.driver = driver
        self.company = company
        self.company_linkedin_url = company_linkedin_url
        self.location = location
        self.full_time = full_time,
        self.experience_years = experience_years,
        self.type = type,
        self.required_skills = required_skills,
        self.needs_experience = needs_experience,
        self.salary = salary,
        self.posted_date = posted_date
        self.applicant_count = applicant_count
        self.job_description = job_description
        self.benefits = benefits

        if scrape:
            self.scrape(close_on_complete)

    def __repr__(self):
        return f"<Job {self.job_title} {self.company}>"

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            raise NotImplemented("This part is not implemented yet")

    def to_dict(self):
        return {
            "linkedin_url": self.linkedin_url,
            "job_title": self.job_title,
            "company": self.company,
            "company_linkedin_url": self.company_linkedin_url,
            "location": self.location,
            "posted_date": self.posted_date,
            "applicant_count": self.applicant_count,
            "job_description": self.job_description,
            "benefits": self.benefits
        }


    def scrape_logged_in(self, close_on_complete=True):
        """
                Scrapes job details from LinkedIn when the user is logged in.

                Args:
                    close_on_complete (bool): Whether to close the WebDriver instance after scraping. Defaults to True.

                Returns:
                    None
                """
        driver = self.driver
        
        driver.get(self.linkedin_url)
        self.focus()
        self.job_title = self.wait_for_element_to_load(name="jobs-unified-top-card__job-title").text.strip()
        self.company = self.wait_for_element_to_load(name="jobs-unified-top-card__company-name").text.strip()
        self.company_linkedin_url = self.wait_for_element_to_load(name="jobs-unified-top-card__company-name").find_element_by_tag_name("a").get_attribute("href")
        self.location = self.wait_for_element_to_load(name="jobs-unified-top-card__bullet").text.strip()
        self.posted_date = self.wait_for_element_to_load(name="jobs-unified-top-card__posted-date").text.strip()
        try:
            self.applicant_count = self.wait_for_element_to_load(name="jobs-unified-top-card__applicant-count").text.strip()
        except TimeoutException:
            self.applicant_count = 0
        job_description_elem = self.wait_for_element_to_load(name="jobs-description")
        self.mouse_click(job_description_elem.find_element_by_tag_name("button"))
        job_description_elem = self.wait_for_element_to_load(name="jobs-description")
        job_description_elem.find_element_by_tag_name("button").click()
        self.job_description = job_description_elem.text.strip()
        try:
            self.benefits = self.wait_for_element_to_load(name="jobs-unified-description__salary-main-rail-card").text.strip()
        except TimeoutException:
            self.benefits = None

        if close_on_complete:
            driver.close()

import job_search, actions
from selenium import webdriver

driver = webdriver.Chrome()
email = "naulub@makobj.store"
password = "Fishpassword"
actions.login(driver, email, password)

job_search = job_search.JobSearch(driver=driver, close_on_complete=False, scrape=False)
# job_search contains jobs from your logged in front page:
# - job_search.recommended_jobs
# - job_search.still_hiring
# - job_search.more_jobs

job_listings = job_search.search("Machine Learning Engineer") # returns the list of `Job` from the first page

print(job_listings)
import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from database_functions import add_data_to_db
import job_search, actions
from selenium import webdriver
import csv
from openai import OpenAI
def extract_job_data(jobs):

  job_data = []
  for job in jobs:
    job_data.append(
        (
            job.job_title,
            job.linkedin_url,
            job.company,
            job.location,
            job.posted_date,
            job.applicant_count,
            job.job_description,
        )
    )
  return job_data
def write_jobs_to_csv(jobs, filename="jobs.csv"):


    with open(filename, "w", newline="") as csvfile:
        fieldnames = list(jobs[0].to_dict().keys())  # Get column names from first job
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write CSV header row
        job_data = [job.to_dict() for job in jobs]  # Convert all jobs to dictionaries
        writer.writerows(job_data)  # Write all job data at once


def create_browser_session():
    driver = webdriver.Chrome()
    # Implement your specific login logic here (similar to login_to_account above)
    # ...
    email = "ziicug@makobj.store"
    password = "Fishpassword"
    actions.login(driver, email, password)
    return driver

def save_session(driver, cookies_file):
    cookies = driver.get_cookies()
    with open(cookies_file, 'wb') as f:
        pickle.dump(cookies, f)

def load_session(driver,cookies_file):
    # driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/feed/")
    with open(cookies_file, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver

def main():
    try:
        driver = webdriver.Chrome()
        driver = load_session(driver,"saved_session.pkl")  # Attempt to load existing session
        driver.get("https://www.linkedin.com/")
        print("Loaded existing session")
    except (FileNotFoundError,EOFError,TypeError):
        driver = create_browser_session()
        save_session(driver, "saved_session.pkl")  # Save for future use
        print("Created and saved new session")


    job_srch = job_search.JobSearch(driver=driver, close_on_complete=False, scrape=False)
    job_listings = job_srch.search("software engineer")  # returns the list of `Job` from the first page
    # write_jobs_to_csv(job_listings, "software_engineer_jobs.csv")
    data = extract_job_data(job_listings)
    add_data_to_db(data)
    driver.quit()  # Close the browser session

if __name__ == "__main__":
    main()









# input : a list of jobs , and optionally filename for the csv file
#output : a csv file with all jobs data provided

driver = webdriver.Chrome()
email = "ziicug@makobj.store"
password = "Fishpassword"
actions.login(driver, email, password)



# client = OpenAI()

job_search = job_search.JobSearch(driver=driver, close_on_complete=False, scrape=False)
job_listings = job_search.search("software engineer") # returns the list of `Job` from the first page

# Example usage:
write_jobs_to_csv(job_listings,"software_engineer_jobs.csv")  # Write to jobs.csv

print(len(job_listings))
# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system",
#          "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#         {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#     ]
# )
#
# print(completion.choices[0].message)

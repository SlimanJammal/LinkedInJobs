import os

import job_search, actions
from selenium import webdriver
import csv
from openai import OpenAI

# input : a list of jobs , and optionally filename for the csv file
#output : a csv file with all jobs data provided
def write_jobs_to_csv(jobs, filename="jobs.csv"):


    with open(filename, "w", newline="") as csvfile:
        fieldnames = list(jobs[0].to_dict().keys())  # Get column names from first job
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write CSV header row
        job_data = [job.to_dict() for job in jobs]  # Convert all jobs to dictionaries
        writer.writerows(job_data)  # Write all job data at once

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

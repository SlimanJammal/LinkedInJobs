import os

import job_search, actions
from selenium import webdriver

# driver = webdriver.Chrome()
# email = "rutjub@makobj.store"
# password = "qwerty1234"
# actions.login(driver, email, password)
#
# job_search = job_search.JobSearch(driver=driver, close_on_complete=False, scrape=False)
# # job_search contains jobs from your logged in front page:
# # - job_search.recommended_jobs
# # - job_search.still_hiring
# # - job_search.more_jobs
#
# job_listings = job_search.search("Machine Learning Engineer") # returns the list of `Job` from the first page
#
# print(job_listings)


from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system",
         "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
)

print(completion.choices[0].message)

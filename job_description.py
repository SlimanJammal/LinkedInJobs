import pandas as pd
from jobs import Job




# def experience_by_job():

df = pd.read_csv("jobs.csv")

jobs_list = []

for index, row in df.iterrows():
    job = Job(
        linkedin_url=row['linkedin_url'],
        job_title=row['job_title'],
        company=row['company'],
        company_linkedin_url=row['company_linkedin_url'],
        location=row['location'],
        posted_date=row['posted_date'],
        applicant_count=row['applicant_count'],
        job_description=row['job_description'],
        benefits=row['benefits']
    )
    jobs_list.append(job)



import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME')

endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'


def add_to_airtable(data_):
    headers = {
        "Authorization": f'Bearer {AIRTABLE_API_KEY}',
        "Content-Type": "application/json"
    }

    data = data_
    r = requests.post(endpoint, json=data, headers=headers)
    print(r.status_code)


def add_jobs_list_to_airtable(jobs_list):
    data = []
    for job in jobs_list:
        record = {"fields": {"job_title": job[0],
                             "company": job[1],
                             "experience": job[2],
                             "location": job[3],
                             "job_type": job[4],
                             "link": job[5]
                             }
                  }

        data.append(record)
    data_ = {"records": data}
    add_to_airtable(data_)


jobs_list_temp = [['Job Title', 'Company', 'experience', 'Location', 'Job Type', 'link'],
                  ['Job Title', 'Company', 'experience', 'Location', 'Job Type', 'link'],
                  ['Job Title', 'Company', 'experience', 'Location', 'Job Type', 'link']]


add_jobs_list_to_airtable(jobs_list_temp)

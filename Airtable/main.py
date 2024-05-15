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
    # print(r.content)
    print(r.status_code)
    print(r.json())



# input list of jobs
def add_jobs_list_to_airtable(jobs_list):
    data = []
    size = 0
    for job in jobs_list:
        record = {
                  "fields": {"job_title": job[0],
                             "company": job[1],
                             "experience": job[2],
                             "experience_description": job[3],
                             "location": job[4],
                             "job_type": job[5],
                             "skills": job[6],
                             "link": job[7]
                             }
                  }

        data.append(record)
        size += 1
        # max number to add in patch is 10
        if size == 10:
            data_ = {"records": data,"typecast": True}
            add_to_airtable(data_)
            data = []
            size = 0

    if len(data):
        data_ = {"records": data,"typecast": True}
        add_to_airtable(data_)

skills = ['a','b']
jobs_list_temp = [
    ['Software Engineer', 'ABC Company','Experience needed' , '3 years', ['New York'], 'Full-time',skills , 'https://example.com/job1'],
    ['Data Scientist', 'XYZ Corporation', 'Experience needed', '2 years', ['San Francisco'], 'Remote',skills , 'https://example.com/job2'],
    ['Product Manager', '123 Enterprises', 'Experience needed', '5 years', ['London'], 'Part-time',skills , 'https://example.com/job3'],
    ['UX Designer', 'Tech Innovations Ltd.', 'Experience needed', '4 years', ['Berlin'], 'Full-time',skills , 'https://example.com/job4'],
    ['Marketing Analyst', 'Global Marketing Solutions', 'Experience needed', '3 years', ['Paris'], 'Contract',skills , 'https://example.com/job5'],
    ['Financial Analyst', 'Finance Unlimited', 'Experience needed', '2 years', ['Tokyo'], 'Full-time',skills , 'https://example.com/job6'],
    ['Software Developer', 'Tech Solutions Inc.', 'None', '3 years', ['Sydney'], 'Remote',skills , 'https://example.com/job7'],
    ['HR Manager', 'Human Resources Experts', 'None', '5 years', ['Toronto'], 'Full-time',skills , 'https://example.com/job8'],
    ['Sales Representative', 'SalesPro', 'None', '1 year', ['Dubai'], 'Commission-based',skills , 'https://example.com/job9'],
    ['Graphic Designer', 'Creative Designs Co.', 'None', '2 years', ['Los Angeles'], 'Part-time',skills , 'https://example.com/job10']

]
# jobs_list_temp = [["a","dfsasda","None","sadasd",["New York"],"part time",["fffff"],"wwww.google.com"]]
add_jobs_list_to_airtable(jobs_list_temp)



def delete_all_records():
    base_url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(base_url, headers=headers)
    data = response.json()
    record_ids = [record['id'] for record in data['records']]
    for record_id in record_ids:
        delete_url = f'{base_url}/{record_id}'
        requests.delete(delete_url, headers=headers)
    print("All records have been deleted.")


# delete_all_records()

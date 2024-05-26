import requests
import os
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_TABLE_NAME_1 = os.environ.get('AIRTABLE_TABLE_NAME_1')
AIRTABLE_TABLE_NAME_2 = os.environ.get('AIRTABLE_TABLE_NAME_2')
AIRTABLE_TABLE_NAME_3 = os.environ.get('AIRTABLE_TABLE_NAME_3')


# computer science, electrical eng, mechanical eng
def get_table_name_by_field(field_name):
    if field_name == "CS":
        return AIRTABLE_TABLE_NAME_1
    elif field_name == "EE":
        return AIRTABLE_TABLE_NAME_2
    elif field_name == "ME":
        return AIRTABLE_TABLE_NAME_3


def add_to_airtable(data_, field_name):
    """
        Adds data to the specified Airtable.

        Args:
            data_ (dict): The data to be added to the Airtable.
            field_name (str): The field name specifying the type of job (e.g., 'CS', 'EE', 'ME').

        Returns:
            None
        """
    endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{get_table_name_by_field(field_name)}'
    headers = {
        "Authorization": f'Bearer {AIRTABLE_API_KEY}',
        "Content-Type": "application/json"
    }

    data = data_
    r = requests.post(endpoint, json=data, headers=headers)
    # print(r.content)
    if r.status_code != 200:
        print(r.status_code)
        print(r.json())


# input list of jobs
def skills_to_list(skills_):
    skills_list = skills_.split(",")

    return skills_list


def add_jobs_list_to_airtable(jobs_list, field_name):
    """
        Adds a list of job records to the specified Airtable.

        Args:
            jobs_list (list): A list of job records, where each record is a list containing
                job details such as title, company, experience, etc.
            field_name (str): The field name specifying which Airtable to add the records to.

        Returns:
            None
        """
    data = []
    size = 0
    for job in jobs_list:
        record = {
            "fields": {"job_title": job[0],
                       "company": job[2],
                       "experience": job[12],
                       "experience_years": job[9],
                       "posting_time": job[3],
                       "applicant_count": job[4],
                       "location": job[2],
                       "job_type": job[8],
                       "degree_type": job[10],
                       "skills": skills_to_list(job[11]),
                       "link": job[6]
                       }
        }

        data.append(record)
        size += 1
        # max number to add in patch is 10
        if size == 10:
            data_ = {"records": data, "typecast": True}
            add_to_airtable(data_, field_name)
            data = []
            size = 0

    if len(data):
        data_ = {"records": data, "typecast": True}
        add_to_airtable(data_, field_name)


# field name options "CS","EE","ME"
def delete_all_records(field_name):
    """
        Deletes all records from the specified Airtable.

        Args:
            field_name (str): The field name specifying which Airtable to delete records from.
            CS, EE and ME
        Returns:
            None
        """
    base_url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{get_table_name_by_field(field_name)}'
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
    print(f"All records In {field_name} airtable have been deleted.")




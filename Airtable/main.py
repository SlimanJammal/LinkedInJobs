import requests
import os
from dotenv import load_dotenv
load_dotenv(".env")
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME')


endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'



def add_to_airtable(name="", email="", address=""):
    headers = {
        "Authorization": f'Bearer {AIRTABLE_API_KEY}',
        "Content-Type": "application/json"
    }

    data = {
        "records": [
            {
                "fields": {
                    "name": name,
                    "email": email
                }
            }
        ]
    }
    r = requests.post(endpoint, json=data, headers=headers)
    print(r.status_code)



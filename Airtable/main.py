import requests
AIRTABLE_BASE_ID = ""
AIRTABLE_API_KEY = ""
AIRTABLE_TABLE_NAME = ""

endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

headers = {
    "Authorization": f'Bearer {AIRTABLE_API_KEY}',
    "Content-Type": "application/json"
}

data = {
  "records": [
    {
      "fields": {
          "name":"alex",
          "email":"<EMAIL>"
      }
    },
    {
      "fields": {}
    }
  ]
}


r = requests.post(endpoint, json=data, headers=headers)
print(r.status_code)


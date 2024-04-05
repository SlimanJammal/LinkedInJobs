from datetime import datetime

import mysql.connector
import credintials
from openai import OpenAI


def connect_to_db():
    try:
        with open('db_pass.txt', 'r') as file:
            password = file.readline().strip()
    except FileNotFoundError:
        print("Error: db_pass.txt not found")

    return mysql.connector.connect(host=credintials.db_host, user=credintials.db_user, password=credintials.db_password,
                                   database=credintials.db_name)


def create_db():
    db = mysql.connector.connect(host=credintials.db_host, user=credintials.db_user, password=credintials.db_password)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS initdb")
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Jobs")
    cursor.execute(
        "Create Table Jobs (title TEXT NOT NULL,job_url TEXT NOT NULL,company_name TEXT NOT NULL,location TEXT NOT NULL,posted_date TEXT NOT NULL,applications_count TEXT NOT NULL,job_description TEXT NOT NULL,id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
    db.commit()
    cursor.close()
    db.close()


def orig_add_data_to_db(data):
    db = connect_to_db()
    cursor = db.cursor()

    sql = "INSERT INTO Jobs (title,job_url,company_name,location,posted_date,applications_count,job_description) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql, data)
    # Commit the changes
    db.commit()
    print(cursor.rowcount, "records inserted.")
    cursor.close()
    db.close()


def fetch_jobs_data():
    print("Fetching Jobs Data...")
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Jobs")
    jobs_data = cursor.fetchall()
    cursor.close()
    db.close()
    jobs_dict = {}
    for job_data in jobs_data:
        job_id = job_data.pop("id")
        jobs_dict[job_id] = job_data
    return jobs_dict


def generate_job_fields(job_data):
    # todo we need to fix this function, chatgpt out is wrong. and acces of completion is incorrect.
    print("Generating job fields")
    client = OpenAI()
    messages = []
    messages.append({
        "role": "system",
        "content": "you are given a list of jobs, each message of the following is a job, with it's attributes - job title,"
                   " company name, location, job url and job description."
    })
    temp_index = 0 #todo remove- testing only
    for job_id, job_details in job_data.items():
        if temp_index == 10:
            break
        message = {"role": "user",
                   "content": f"Title: {job_details['title']}, Company Name: {job_details['company_name']}, Location: {job_details['location']}, Job URL: {job_details['job_url']}, Job Description: {job_details['job_description']}."}
        messages.append(message)

        temp_index +=1

    messages.append({
        "role": "system",
        "content": "You need to return for each job the following (separate the attributes for each job by a #)"
                   " fields  Employment Type: Full Time/Part time,Work Experience Level Needed: number of years in int"
                   " could be 0 too, "
                   "Education Requirements: None/Bsc/MSC/PHD and the field, Skills and Qualifications: write them"
                   " in a list i.e [skill1,skill2,skill3]. Separate each jobs data's with **** (when finishing the data about a job write ****) "
    })
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    returned_msg = completion.choices[0].message
    print(returned_msg)
    try:
        with open('gpt_out_msg.txt', 'w') as file:
            file.write(returned_msg.content)
        print("Content successfully written to the file.")
    except IOError:
        print("Error: Unable to write to the file.")
    generated_fields = []
    # for i, job_id in enumerate(job_data):
    #     generated_fields.append({"job_id": job_id, "fields":completion.choices[0].message["content"]})

    return generated_fields


def create_processed_jobs_table():
    print("Creating processed jobs table...")
    db = connect_to_db()
    cursor = db.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS ProcessedJobs (
        job_id INT PRIMARY KEY,
        processed_fields TEXT
    )
    """
    cursor.execute(create_table_query)
    db.commit()
    cursor.close()
    db.close()


def insert_processed_fields(processed_fields):
    print("Inserting processed")
    db = connect_to_db()
    cursor = db.cursor()
    for job in processed_fields:
        job_id = job["job_id"]
        fields = job["fields"]
        insert_query = "INSERT INTO ProcessedJobs (job_id, processed_fields) VALUES (%s, %s)"
        cursor.execute(insert_query, (job_id, fields))
    db.commit()
    cursor.close()
    db.close()

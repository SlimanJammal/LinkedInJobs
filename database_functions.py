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


def get_no_experience_jobs(job_data):

    print("Generating job fields")

    client = OpenAI()
    messages = []
    messages.append({
        "role": "user",
        "content": ""
    })

    answers = []
    temp_index = 0
    for job_id, job_details in job_data.items():
        try:
            message = {"role": "user",
                       "content": f"does this job need experience answer yes/no only. Title: {job_details['title']}, Index: {temp_index+1}, Job Description: {job_details['job_description']}."}
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[message]
            )

            answers.append([job_details['title'],completion.choices[0].message.content])
        except Exception as e:
            print("gpt error in get_no_experience_jobs")
            print(e)
            if answers[-1][0] != job_details['title']:
                answers.append([job_details['title'], "error"])
        temp_index += 1

    try:
        with open('gpt_out_msg.txt', 'w') as file:
            for answer in answers:
                file.write(str(answer))
        print("Content successfully written to the file.")
    except IOError:
        print("Error: Unable to write to the file.")
    no_experience_list = []
    for i, answer in enumerate(answers):
        if answer[1] == "No" or answer[1] == "no":
            index = i+1
            no_experience_list.append(job_data[index])

    return no_experience_list


def create_no_exp_jobs_table():
    print("Creating processed jobs table...")
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS JobsWithOutExperience")
    cursor.execute(
        "Create Table JobsWithOutExperience (title TEXT NOT NULL,job_url TEXT NOT NULL,company_name TEXT NOT NULL,location TEXT NOT NULL,posted_date TEXT NOT NULL,applications_count TEXT NOT NULL,job_description TEXT NOT NULL,id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
    db.commit()
    cursor.close()
    db.close()


def insert_no_exp_jobs(no_exp_jobs):
    print("Inserting processed")
    db = connect_to_db()
    cursor = db.cursor()

    sql = "INSERT INTO Jobs (title,job_url,company_name,location,posted_date,applications_count,job_description) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql, no_exp_jobs)
    # Commit the changes
    db.commit()
    print(cursor.rowcount, "records inserted.")
    cursor.close()
    db.close()

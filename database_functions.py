from datetime import datetime

import mysql.connector
import credintials
from openai import OpenAI


def connect_to_db():
    return mysql.connector.connect(host=credintials.db_host, user=credintials.db_user, password=credintials.db_password,
                                   database=credintials.db_name)


def create_db():
    db = mysql.connector.connect(host=str(credintials.db_host), user=str(credintials.db_user),
                                 password=str(credintials.db_password))
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS initdb")
    db = connect_to_db()
    cursor = db.cursor()

    table_names = ["JOBS_CS", "JOBS_EE", "JOBS_ME"]
    for table_name in table_names:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"""
            CREATE TABLE {table_name} (
                title TEXT NOT NULL,
                company_name TEXT NOT NULL,
                location TEXT NOT NULL,
                posted_date TEXT NOT NULL,
                applications_count TEXT NOT NULL,
                job_description TEXT NOT NULL,
                job_url VARCHAR(2083) NOT NULL,
                job_id VARCHAR(15) NOT NULL UNIQUE,
                full_time VARCHAR(40) NOT NULL,
                experience VARCHAR(80) NOT NULL,
                degree_type TEXT NOT NULL,
                required_skills TEXT NOT NULL,
                needs_experience TEXT NOT NULL
            )
        """)
    db.commit()
    cursor.close()
    db.close()


def orig_add_data_to_db(data, field_name):
    table_name = f"JOBS_{field_name}"
    db = connect_to_db()
    cursor = db.cursor()

    sql = f"""
        INSERT INTO {table_name} 
        (title, company_name, location, posted_date, applications_count, job_description, job_url, job_id, full_time, experience, degree_type, required_skills, needs_experience) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, data)
    db.commit()
    print(cursor.rowcount, "records inserted.")
    cursor.close()
    db.close()


def fetch_jobs_data(field_name):
    table_name = f"JOBS_{field_name}"
    print(f"Fetching Jobs Data from {table_name}...")
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    jobs_data = cursor.fetchall()
    cursor.close()
    db.close()
    jobs_dict = {}
    for job_data in jobs_data:
        job_id = job_data.pop("id")
        jobs_dict[job_id] = job_data
    return jobs_dict


def create_no_exp_jobs_table():
    print("Creating processed jobs table...")
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS JobsWithOutExperience")
    cursor.execute("""
        CREATE TABLE JobsWithOutExperience (
            title TEXT NOT NULL,
            job_url TEXT NOT NULL,
            company_name TEXT NOT NULL,
            location TEXT NOT NULL,
            posted_date TEXT NOT NULL,
            applications_count TEXT NOT NULL,
            job_description TEXT NOT NULL,
            id int PRIMARY KEY NOT NULL AUTO_INCREMENT
        )
    """)
    db.commit()
    cursor.close()
    db.close()


def insert_no_exp_jobs(no_exp_jobs):
    print("Inserting processed jobs")
    db = connect_to_db()
    cursor = db.cursor()

    sql = """
        INSERT INTO JobsWithOutExperience 
        (title, job_url, company_name, location, posted_date, applications_count, job_description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, no_exp_jobs)
    db.commit()
    print(cursor.rowcount, "records inserted.")
    cursor.close()
    db.close()


def get_data_from_database(field_name):
    table_name = f"JOBS_{field_name}"
    db = connect_to_db()
    cursor = db.cursor()

    urls_sql = f"SELECT * FROM {table_name}"
    cursor.execute(urls_sql)
    jobs = cursor.fetchall()
    cursor.close()
    db.close()
    return jobs


def update_db_data(data, field_name):
    table_name = f"JOBS_{field_name}"
    db = connect_to_db()
    cursor = db.cursor()

    urls_sql = f"SELECT job_id FROM {table_name}"
    cursor.execute(urls_sql)
    existing_urls = [url[0] for url in cursor.fetchall()]

    new_data = [item for item in data if item[7] not in existing_urls]

    if new_data:
        sql = f"""
            INSERT INTO {table_name} 
            (title, company_name, location, posted_date, applications_count, job_description, job_url, job_id, full_time, experience, degree_type, required_skills, needs_experience) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(sql, new_data)
        db.commit()
        print(cursor.rowcount, "new records inserted.")
    else:
        print("No new jobs found to insert.")

    cursor.close()
    db.close()
def get_jobs_salaries(job_data):
  print("Generating job salaries")


  client = OpenAI()

  salaries_list = []
  temp_index = 0

  for job_id, job_details in job_data.items():
    try:
      message = {
        "role": "user",
        "content": f"Please estimate the salary for this job monthly in {job_details['location']} in the currency of {job_details['location']}."
                   f" Title keep the answer shorter than 20 chars: {job_details['title']}, Index: {temp_index + 1}, Job Description: {job_details['job_description']}. Provide a single line estimate of max 20 characters."
      }
      completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[message]
      )

      estimated_salary = completion.choices[0].message.content


      salaries_list.append([job_details['title'], estimated_salary])
    except Exception as e:
      print("GPT error in get_job_salaries")
      print(e)
      if salaries_list[-1][0] != job_details['title']:
        salaries_list.append([job_details['title'], "error"])
    temp_index += 1

  for i, salary in enumerate(salaries_list):
    job_data[list(job_data.keys())[i]]['salary'] = salary[1]

  return job_data

def data_pre_processing(job_data):
    # todo we need to fix this function, chatgpt out is wrong. and acces of completion is incorrect.
    print("Generating job fields")
    client = OpenAI()
    # messages = []
    start_msg = {
        "role": "system",
        "content": "you are given a list of jobs, each message of the following is a job, with it's attributes - job title,"
                   " company name, location, job url and job description."
    }
    end_msg = {
        "role": "system",
        "content": "You need to return for the given job the following fields (separate  by a #)"
                   "   Employment Type: Full Time/Part time , Work Experience Level Needed: number of years in int (could be 0 too), "
                   "Education Requirements: None/Bsc/MSC/PHD and the field, Skills and Qualifications: write them"
                   " in a list i.e skill1,skill2,skill3. and at the end tell me if the job needs work experience yes/no answer ONLY (DO NOT WRITE THE EXPERIENCE NEEDED HERE)  "
                    "result should look like (FUll time # 5 years + # bsc or equevelant # skill1,skill2,skill3 # yes)"
    }

    temp_index = 0 #todo remove- testing only
    returned_msgs = []
    for job in job_data:
        # if temp_index == 10:
        #     break
        messages = []
        messages.append(start_msg)
        message = {"role": "user",
                   "content": f"Title: {job.job_title}, Company Name: {job.company}, Location: {job.location}, Job URL: {job.linkedin_url}, Job Description: {job.job_description}."}
        messages.append(message)
        messages.append(end_msg)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        returned_msgs.append(completion.choices[0].message.content)
        # temp_index +=1



    for i,msg in enumerate(returned_msgs):
        try:
            parts = msg.split("#")
            job_data[i].full_time=parts[0]
            job_data[i].experience_years = parts[1]
            job_data[i].type = parts[2]
            job_data[i].required_skills = parts[3]
            job_data[i].needs_experience = parts[4]
        except Exception as e:
            continue
        # print(parts[-1]) # parts 1) full time / part time 2) experience 3) degree 4) skills

    return job_data

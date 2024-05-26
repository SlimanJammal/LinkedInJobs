from datetime import datetime

import mysql.connector
import credintials
from openai import OpenAI


def connect_to_db():
    """
       Establishes a connection to the MySQL database using credentials provided.

       This function connects to a MySQL database using the host, user, password,
       and database name specified in the `credintials` module.

       Returns:
           mysql.connector.connection.MySQLConnection: A MySQL connection object.
       """

    return mysql.connector.connect(host=credintials.db_host, user=credintials.db_user, password=credintials.db_password,
                                   database=credintials.db_name)


def create_db():
    """
      Creates and initializes a MySQL database with specified tables.

      This function connects to the MySQL server using credentials from the
      `credintials` module and creates a database named 'initdb' if it does not
      already exist. It then creates three tables: 'JOBS_CS', 'JOBS_EE', and 'JOBS_ME'.
      If these tables already exist, they are dropped and recreated with the
      specified schema.

      The tables are designed to store job postings with fields such as title,
      company name, location, posted date, applications count, job description,
      job URL, job ID, full-time status, experience, degree type, required skills,
      and whether experience is needed.

      Returns:
          None
      """
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
                needs_experience TEXT NOT NULL,
                salary TEXT NOT NULL 
            )
        """)
    db.commit()
    cursor.close()
    db.close()


def orig_add_data_to_db(data, field_name):
    """
        Inserts data into a specified table in the database.

        This function takes a list of tuples containing job data and inserts it into
        a table in the MySQL database. The table name is dynamically determined based
        on the provided `field_name` parameter, which is appended to the prefix 'JOBS_'.

        Args:
            data (list of tuples): The job data to be inserted. Each tuple should contain
                the following fields in order: title, company_name, location, posted_date,
                applications_count, job_description, job_url, job_id, full_time, experience,
                degree_type, required_skills, and needs_experience.
            field_name (str): The suffix for the table name to determine which table the
                data will be inserted into (e.g., 'CS', 'EE', 'ME').

        Returns:
            None
        """
    table_name = f"JOBS_{field_name}"
    db = connect_to_db()
    cursor = db.cursor()

    sql = f"""
        INSERT INTO {table_name} 
        (title, company_name, location, posted_date, applications_count, job_description, job_url, job_id, full_time, experience, degree_type, required_skills, needs_experience,salary) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, data)
    db.commit()
    print(cursor.rowcount, "records inserted.")
    cursor.close()
    db.close()


def fetch_jobs_data(field_name):
    """
       Fetches job data from a specified table in the database.

       This function retrieves all job records from a table in the MySQL database.
       The table name is dynamically determined based on the provided `field_name`
       parameter, which is appended to the prefix 'JOBS_'.

       Args:
           field_name (str): The suffix for the table name to determine which table
               the data will be fetched from (e.g., 'CS', 'EE', 'ME').

       Returns:
           dict: A dictionary where each key is a job ID and each value is a dictionary
                 of the job's data (excluding the job ID).
       """
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
    """
       Fetches all data from a specified table in the database.

       This function connects to the MySQL database and retrieves all records from a table.
       The table name is dynamically determined based on the provided `field_name` parameter,
       which is appended to the prefix 'JOBS_'.

       Args:
           field_name (str): The suffix for the table name to determine which table
               the data will be fetched from (e.g., 'CS', 'EE', 'ME').

       Returns:
           list of tuple: A list of tuples containing all records from the specified table.
       """
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
    """
       Updates the database with new job data.

       This function connects to the MySQL database and checks for new job data to insert.
       The table name is dynamically determined based on the provided `field_name` parameter,
       which is appended to the prefix 'JOBS_'.

       Args:
           data (list of tuples): The new job data to be inserted. Each tuple should contain
               the following fields in order: title, company_name, location, posted_date,
               applications_count, job_description, job_url, and job_id.
           field_name (str): The suffix for the table name to determine which table
               the data will be updated in (e.g., 'CS', 'EE', 'ME').

       Returns:
           None
       """
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
            (title, company_name, location, posted_date, applications_count, job_description, job_url, job_id, full_time, experience, degree_type, required_skills, needs_experience, salary) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(sql, new_data)
        db.commit()
        print(cursor.rowcount, "new records inserted.")
    else:
        print("No new jobs found to insert.")

    cursor.close()
    db.close()


def data_pre_processing(job_data):
    """
        Pre-processes job data to extract specific fields using OpenAI GPT-3.5 model.

        This function takes a list of job data objects and pre-processes them to extract
        specific fields such as employment type, work experience level needed, education requirements,
        skills and qualifications, and whether the job requires work experience. It utilizes the
        OpenAI GPT-3.5 model to generate prompts for extracting these fields.

        Args:
            job_data (list): A list of job data objects, each containing attributes such as job title,
                company name, location, job URL, and job description.

        Returns:
            list: A list of updated job data objects with extracted fields.
        """
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
                   " in a list i.e skill1,skill2,skill3. and at the end tell me if the job needs work experience yes/no answer ONLY (DO NOT WRITE THE EXPERIENCE NEEDED HERE) "
                   "Salary:  Estimate job monthly salary Number in give location's currency (e.g. USD, EUR, GBP)  "
                    "result should look like (FUll time # 5 years + # bsc or equevelant # skill1,skill2,skill3 # yes # 20,000 EUR)"
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
            job_data[i].salary = parts[5]
        except Exception as e:
            continue
        # print(parts[-1]) # parts 1) full time / part time 2) experience 3) degree 4) skills

    return job_data

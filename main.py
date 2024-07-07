import pickle
import sys
import database_functions
import job_search, actions
from selenium import webdriver
import csv
import credintials
from apscheduler.schedulers.blocking import BlockingScheduler
from openai import OpenAI

from jobs import Job


# pip install -r requirements.txt

def extract_job_data(jobs):

  job_data = []
  for job in jobs:
    job_data.append(
        (
            job.job_title,
            job.company,
            job.location,
            job.posted_date,
            job.applicant_count,
            job.job_description,
            job.linkedin_url,
            job.linkedin_url.split("/")[5],# job id
            job.full_time,
            job.experience_years,
            job.type,
            job.required_skills,
            job.needs_experience,
            job.salary
        )
    )
  return job_data


# # input : a list of jobs , and optionally filename for the csv file
# #output : a csv file with all jobs data provided

def write_jobs_to_csv(jobs, filename="jobs.csv"):


    with open(filename, "w", newline="") as csvfile:
        fieldnames = list(jobs[0].to_dict().keys())  # Get column names from first job
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write CSV header row
        job_data = [job.to_dict() for job in jobs]  # Convert all jobs to dictionaries
        writer.writerows(job_data)  # Write all job data at once


def create_browser_session():
    driver = webdriver.Chrome()
    # Implement your specific login logic here (similar to login_to_account above)
    # ...
    actions.login(driver, credintials.linkedin_username, credintials.linkedin_password)
    return driver

def save_session(driver, cookies_file):
    cookies = driver.get_cookies()
    with open(cookies_file, 'wb') as f:
        pickle.dump(cookies, f)

def load_session(driver,cookies_file):
    # driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/feed/")
    with open(cookies_file, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver


def get_field_name(field_name):
    if field_name == "CS":
        return "Software Engineer"
    elif field_name == "ME":
            return "Mechanical Engineer"
    elif field_name == "EE":
        return "Electrical Engineer"
    else:
        return "Software Engineer"


def update_database(field_name):
    job_listings = []
    data = []
    try:
        driver = webdriver.Chrome()
        driver = load_session(driver,"saved_session.pkl")  # Attempt to load existing session
        driver.get("https://www.linkedin.com/")
        print("Loaded existing session")
    except (FileNotFoundError,EOFError,TypeError):
        driver = create_browser_session()
        save_session(driver, "saved_session.pkl")  # Save for future use
        print("Created and saved new session")

    try:
        job_srch = job_search.JobSearch(driver=driver, close_on_complete=False, scrape=False)
        print("Job Search")
        job_listings = job_srch.search(get_field_name(field_name))
    except Exception as e:
        print("Error During job search: " + str(e))

    try:
        data = extract_job_data(job_listings)
        processed_data = database_functions.data_pre_processing(job_listings)
        data = extract_job_data(processed_data)
    except Exception as e:
        print(e)
        print("Data could not be extracted")
    try:
        database_functions.update_db_data(data, field_name)
    except Exception as e:
        print(e)
        print("Error updating database")
    driver.quit()


def read_jobs_from_csv(csv_file_path):
    """
    Reads jobs data from a CSV file and creates a list of Job objects.

    Args:
        csv_file_path (str): Path to the CSV file containing job data.

    Returns:
        list[Job]: A list of Job objects representing the job data.
    """

    jobs = []
    with open(csv_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            job = Job(
                linkedin_url=row.get("linkedin_url", None),
                job_title=row.get("job_title", None),
                company=row.get("company", None),
                location=row.get("location", None),
                posted_date=row.get("posted_date", None),
                applicant_count=row.get("applicant_count", None),
                job_description=row.get("job_description", None),
                scrape=False
            )

            jobs.append(job)
    return jobs




# this function will be called only once at the start-up of the DataBase
def initialization() -> None:
    database_functions.create_db()
    print("Initialization Finished")



if __name__ == "__main__":


    field_name = None
    if len(sys.argv) > 1:
        if sys.argv[1:][0] == "CS" or sys.argv[1:][0] == "EE" or sys.argv[1:][0] == "ME":
            if len(sys.argv) > 2 and sys.argv[1:][1] == "DB_CREATE":
                initialization()
                print("Creating New DB")
            else:
                print("Updating Old DB")

            print("Searching Jobs In", sys.argv[1:][0])
            field_name = sys.argv[1:][0]
        else:
            print("Wrong Input")
            exit(0)
    else:
        print("No Arguments Provided.")
        exit(0)



    # scheduler = BlockingScheduler()
    # scheduler.add_job(update_database, 'interval', hours=12, minutes=0, seconds=0)
    # scheduler.start()'

    # airtable.delete_all_records(field_name)
    # initialization()
    # field_name ="CS"
    update_database(field_name)
    # jobs = database_functions.get_data_from_database(field_name)
    # airtable.add_jobs_list_to_airtable(jobs, field_name)





    print("")

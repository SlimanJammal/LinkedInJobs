from datetime import datetime

import mysql.connector




# cursor.execute("CREATE DATABASE testdatabase")


# cursor.execute("Create Table Test (name varchar(50) NOT NULL,created datetime NOT NULL,gender Enum('male','female') NOT NULL,id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
# cursor.execute("INSERT INTO Test (name,created,gender) VALUES(%s,%s,%s)", ("mostfa",datetime.now(),"male"))

# db = mysql.connector.connect(host="localhost", user="root", password="Fishpassword", database="testdatabase")
# cursor = db.cursor()
# # cursor.execute("DROP TABLE IF EXISTS Jobs")
#
#
# cursor.execute("Create Table Jobs (title varchar(150) NOT NULL,job_url varchar(1512) NOT NULL,company_name varchar(150) NOT NULL,location varchar(250) NOT NULL,posted_date varchar(150) NOT NULL,applications_count varchar(150) NOT NULL,job_description varchar(5000) NOT NULL,id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
# db.commit()

title = "Job Title"
job_url = "Job url"
company_name = "company name"
location = "job location"
posted_date = "13 10 99"
applications_count = "100"
job_description = "About the jobFlex Storage Inc., an established and well-funded start-up specializing in self-storage services, is currently seeking a highly skilled and experienced Full-Stack Developer to join our dynamic and innovative Israeli team in Tel-Aviv.As a Full-Stack Developer, you will be responsible for both Node JS backend and Angular 15 frontend development, contributing to a complex and groundbreaking technological project. Your work will directly impact the success of our company and contribute to our mission of revolutionizing the self-storage industry.This position is a key role within our organization, reporting directly to the Chief Technology Officer (CTO). It offers significant growth potential, with the opportunity to eventually advance to a Team Leader position.Key Responsibilities:Collaborate with the team to develop and maintain the Node JS backend and ReactJS/Angular (latest) frontend components of our innovative project.Contribute to the design, development, and implementation of new features and functionalities.Ensure the scalability, performance, and security of the applications.Requirements and Qualifications:Demonstrated experience as a Full-Stack JavaScript Developer for a minimum of 3 years.Strong interpersonal skills and the ability to work effectively within a team environment.Self-motivated, reliable, and capable of working independently when required.Advantages:Experience with Docker, GIT, and MongoDB.Proficiency in working with Google Cloud technologies.  Join us in shaping the future of self-storage services and be part of an exciting journey with tremendous growth potential. If you meet the qualifications and are passionate about cutting-edge technology and innovation, we look forward to hearing from you."

# cursor.execute("INSERT INTO Jobs (title,job_url,company_name,location,posted_date,applications_count,job_description) VALUES(%s,%s,%s,%s,%s,%s,%s)", (title,job_url,company_name,location,posted_date,applications_count,job_description))
#
#
#
#
# db.commit()
#


def add_data_to_db(data):
    db = mysql.connector.connect(host="localhost", user="root", password="Fishpassword", database="testdatabase")
    cursor = db.cursor()

    sql = "INSERT INTO Jobs (title,job_url,company_name,location,posted_date,applications_count,job_description) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql, data)
    # Commit the changes
    db.commit()
    print(cursor.rowcount, "records inserted.")
    cursor.close()
    db.close()
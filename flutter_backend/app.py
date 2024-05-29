from flask import Flask, request, jsonify
from flask_cors import CORS
import credintials
import mysql.connector
from fpdf import FPDF
from openai import OpenAI

import requests
app = Flask(__name__)
CORS(app)

def connect_to_database():
    return mysql.connector.connect(host=credintials.db_host, user=credintials.db_user, password=credintials.db_password,
                                   database=credintials.db_name)

@app.route('/get_jobs', methods=['POST'])
def get_jobs():
    connection = connect_to_database()
    cursor = connection.cursor()

    # Replace with your actual SELECT query
    cursor.execute("SELECT * FROM JOBS_CS")
    data = cursor.fetchall()

    # Convert data to a JSON-friendly format
    card_list = []
    for row in data:
        flag = False
        if row[12].strip() == "yes" or row[12] == "Yes":
            flag = True
        onsite = "Hybrid"
        if "On-site" in row[2]:
            onsite = "On-site"
        card_list.append({
            "Job Title": row[0].split("\n", 1)[0],  # Job title
            "Company Name": row[1],  # Company name
            "Location": row[2],  # Location
            "Is Remote": onsite == "Hybrid",
            "When Posted": row[3],  # When posted
            "Applicants": row[4],  # Number of applicants
            "Job Description": row[5],  # Job description
            "Url": row[6],  # Url
            "Job ID": row[7],  # Job ID
            "Full Time": row[8] == "Full Time",  # Full time (convert to bool)
            "Years Experience": row[9],  # Number of years experience
            "Degree Type": row[10],  # Degree type
            "Skills": row[11],  # Skills (split into a list)
            "Needs Experience": row[12].strip().lower() == "yes", # Remote (convert to bool)
            "Salary estimate": row[13]
        })

    cursor.close()
    connection.close()
    return jsonify(card_list)







'''**************************************** cv generate functions ******************************************** '''



class CV:
    def __init__(self, full_name="", email="", phone="", address="", linkedin="", career_objective="",
                 education="", work_experience="", skills="", certifications="", projects="", awards="",
                 professional_affiliations="", references=""):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.address = address
        self.linkedin = linkedin
        self.career_objective = career_objective
        self.education = education
        self.work_experience = work_experience
        self.skills = skills
        self.certifications = certifications
        self.projects = projects
        self.awards = awards
        self.professional_affiliations = professional_affiliations
        self.references = references

    def get_structure(self):

        data = f"# {self.full_name.replace("\"","")}\n\n"
        data += f"Email: {self.email.replace("\"","")} | Phone: {self.phone.replace("\"","")}\n| "
        data += f"Address: {self.address.replace("\"","")}| \n"
        data += f"LinkedIn: {self.linkedin.replace("\"","")}\n\n"
        if self.career_objective != "":
            data += "## Career Objective\n\n"
            data += f"{self.career_objective.replace("\"","")}\n\n"

        if len(self.education) != 0:
            data += "## Education\n\n"
            for edu in self.education:
                data += f"- **{edu['degree']}** in {edu['institution']}, {edu['years']}\n"
                data += f"  {edu['details']}\n\n"
        if len(self.work_experience) != 0:
            data += "## Work Experience\n\n"
            for exp in self.work_experience:
                data += f"- **{exp['job_title']}** at {exp['company']}, {exp['years']}\n"
                data += f"  {exp['responsibilities']}\n\n"
        if len(self.skills) != 0:
            data += "## Skills\n\n"
            data+= f"- "

            for skill in self.skills:
                skill = skill.replace("[", "").replace("]", "").replace("\"","")
                data += skill
                data += ", "
            data+= "\n\n"



        if len(self.certifications) != 0:
            data += "## Certifications\n\n"
            for cert in self.certifications:
                data += f"- {cert['name']} from {cert['institution']}, {cert['year']}\n"

        if len(self.projects) != 0:
            data += "\n## Projects\n\n"
            for proj in self.projects:
                data += f"- **{proj['name']}**: {proj['description']}\n"

        if len(self.awards) != 0:
            data += "\n## Awards\n\n"
            for award in self.awards:
                data += f"- {award['name']} from {award['institution']}, {award['year']}\n"

        if len(self.professional_affiliations) != 0:
            data += "\n## Professional Affiliations\n\n"
            for aff in self.professional_affiliations:
                data += f"- {aff['role']} at {aff['organization']}, {aff['years']}\n"

        if len(self.references) != 0:
            data += "\n## References\n\n"
            for ref in self.references:
                data += f"- {ref['name']}, {ref['position']} | Contact: {ref['contact']}\n"

        return data




def convert_to_pdf(data):

    Resume_file = "Resume.pdf"
    engine = "weasyprint"
    # Define CSS styles for the PDF
    cssfile = """
                body{
                    padding: 0px;
                    margin:0px;
                }
                h1 {
                color: MidnightBlue;
                margin:0px;
                padding:0px;

                }
                h3{
                    color: MidnightBlue;
                    padding-bottom:0px; 
                    margin-bottom:0px; 
                }
                li{
                    margin-top:5px;
                }

                """
    # API endpoint for converting Markdown to PDF
    url = "https://md-to-pdf.fly.dev"

    # Data to be sent in the POST request
    data = {
        'markdown': data,
        'css': cssfile,
        'engine': engine
    }

    # Send a POST request to the API
    response = requests.post(url, data=data)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Save the generated PDF to a file
        with open(Resume_file, 'wb') as f:
            f.write(response.content)
        print(f"PDF saved to {Resume_file}")
        return response.content
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None





def parse_data_string(data_str):
    data_segments = data_str.split("#")

    parsed_data = {}

    for segment in data_segments:
        if segment.strip():
            key, value = segment.strip().split("=")
            key = key.strip()
            if key == "skills":
                value = [skill.strip() for skill in value.split(",")]
            elif key == "education" or key == "work_experience" or key == "certifications" or key == "projects" or key == "awards" or key == "professional_affiliations" or key == "references":
                value = eval(value)
            parsed_data[key] = value

    return parsed_data

@app.route('/generate_cv', methods=['POST'])
def generate_cv():
    data = request.json
    job_description = data.get('job_description')
    user_info = data.get('user_info', {})

    # Debug: print received data
    print('Job Description:', job_description)
    print('User Info:', user_info)

    example_response  = """
full_name="John Doe"#
email="john.doe@example.com"#
phone="+1234567890"#
address="123 Main St, Anytown, AT 12345"#
linkedin="https://www.linkedin.com/in/johndoe"#
career_objective=""#
education=[
    {
        'degree': 'B.Sc. in Computer Science',
        'institution': 'University of Example',
        'years': '2015-2019',
        'details': 'Graduated with honors, relevant coursework includes Data Structures, Algorithms, and Web Development.'
    },
    {
        'degree': 'M.Sc. in Software Engineering',
        'institution': 'Example Institute of Technology',
        'years': '2019-2021',
        'details': 'Thesis on machine learning algorithms and their applications in real-world problems.'
    }
]#
work_experience=[
    {
        'job_title': 'Software Developer',
        'company': 'Tech Solutions Inc.',
        'location': 'Example City',
        'years': '2021-Present',
        'responsibilities': 'Developed web applications using .NET and AngularJS, collaborated with cross-functional teams, and contributed to code reviews and system design.'
    },
    {
        'job_title': 'Intern',
        'company': 'Startup XYZ',
        'location': 'Example Town',
        'years': 'Summer 2020',
        'responsibilities': 'Assisted in developing mobile applications, performed software testing, and provided technical support to the development team.'
    }
]#
skills=["Python", "JavaScript", "React", "Machine Learning", "Project Management"]#
certifications=[
    {
        'name': 'Certified Scrum Master',
        'institution': 'Scrum Alliance',
        'year': '2022'
    }
]#
projects=[
    {
        'name': 'Personal Portfolio Website',
        'description': 'Designed and developed a personal portfolio website using React and Node.js to showcase my projects and skills.'
    },
    {
        'name': 'Machine Learning Model for Predicting Stock Prices',
        'description': 'Developed a predictive model using Python and scikit-learn to forecast stock prices based on historical data.'
    }
]#
awards=[
    {
        'name': "Dean's List",
        'institution': 'University of Example',
        'year': '2019'
    }
]#
professional_affiliations=[
    {
        'organization': 'IEEE',
        'role': 'Member',
        'years': '2020-Present'
    }
]#
references=[
    {
        'name': 'Jane Smith',
        'position': 'Manager at Tech Solutions Inc.',
        'contact': 'jane.smith@example.com'
    }
]
"""
    msgs = []
    client = OpenAI()
    msg1 = {"role": "user",
         "content": f"for the next msg Generate a one page CV return fields seperated by a #:"
                    f"this is an (don't generate for it) example response: {example_response} "





         }
    msg2 = {"role": "user",
         "content": f"generate for this using the same structure in the example response. Job Description: {job_description}\n"
                    f"User Info: {user_info}\n"
         }

    msgs.append(msg1)
    msgs.append(msg2)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=msgs
    )
    cv_text = completion.choices[0].message.content
    print(cv_text)

    data = parse_data_string(cv_text)
    cv_new = CV(**data)
    pdf_res = convert_to_pdf(cv_new.get_structure())
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaa")

    return jsonify({'cv_pdf': pdf_res})

if __name__ == '__main__':
    app.run(debug=True)

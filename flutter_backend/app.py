from flask import Flask, request, jsonify
from flask_cors import CORS
import credintials
import mysql.connector

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



@app.route('/generate_cv', methods=['POST'])
def generate_cv():
    data = request.json
    job_description = data.get('job_description')
    user_info = data.get('user_info', {})

    # You can print the job description and user info
    print('Job Description:', job_description)
    print('User Info:', user_info)

    # For demonstration purposes, just returning the received data
    return jsonify({
        'job_description': job_description,
        'user_info': user_info
    })

if __name__ == '__main__':
    app.run(debug=True)

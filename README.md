# LinkedIn Jobs

## Description
LinkedIn Jobs is a project designed to improve the job search experience by scraping job listings from LinkedIn, processing them using the ChatGPT API, and storing them in a MySQL database. The project includes a web application that hosts the processed job listings and offers a CV generation feature.

## Purpose
We created this project to address issues with the LinkedIn job search window, such as irrelevant job listings and ineffective experience level filters.

## Features
- Web scraper for LinkedIn job listings
- Processing of job listings using ChatGPT API
- Storage of job listings in a MySQL database
- Web application for viewing job listings
- CV generation tool

## Technology Stack
- **Python**: For the web scraper and backend development
- **Flask**: For the backend of the web application
- **Flutter and Dart**: For the frontend of the web application
- **MySQL**: For database storage

## System Requirements
No specific system requirements.

## Installation Instructions


### Step-by-Step Guide

#### 1. Clone the repository
```bash
git clone <repository-url>
cd project-root

```
#### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

#### 3. Install dependencies

you can see all the dependencies required in the requirements.txt file

``` bash
pip install -r requirements.txt

```
#### 4. Set up the MySQL database
  - [ Install MySQL if not already installed ](https://dev.mysql.com/doc/workbench/en/)
  - Create a new database.
  - Update the database configuration in credintials.py with your MySQL credentials.

    

#### 5. Configuration
Update the following configurations in credintials.py:

- MySQL database connection details
- Linkedin details

then we have to add chatgpt API key to your environment variables,
 to do that follow step 2 (Set Up API Key) [here.](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)


#### 6. Usage
1) Run the scraper to populate the database with job listings.
   ``` bash
   python main.py <FIELD> [OPTION]
   ```
   <FIELD>: Specify the field of interest using one of the following options:
     -  EE for Electrical Engineering.
     -  CS for Computer Science.
     -  ME for Mechanical Engineering.
   [OPTION] (Optional):
    DB_CREATE: Use this option to create or update the database. It deletes all existing data and creates new tables.

  Example:
  ``` bash
   python main.py CS DB_CREATE
  ```
  If the database is already created, you can run:
  ``` bash
   python main.py CS
   ```
  

2) Start the web application to view job listings and generate CVs.
   ```
   some code here
   ```
#### 7. Development Setup

- Follow the installation instructions to set up the project.
- Make sure to activate the virtual environment before making changes.
- Use proper branching and pull requests for contributions.



### Contribution Guidelines
1) Fork the repository.
2) Create a new branch (git checkout -b feature/your-feature-name).
3) Commit your changes (git commit -am 'Add some feature').
4) Push to the branch (git push origin feature/your-feature-name).
5) Create a new Pull Request.


### Contact Information
For support or questions, please contact [Muhammad Eid](https://github.com/Mohammad-Eid) / [Sliman Jammal](https://github.com/SlimanJammal).



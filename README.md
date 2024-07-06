# LinkedIn Jobs

**This project was done under the  supervision of Prof. Roi Poranne as part of a semester project for a BSc in computer science at the University of Haifa.**

**the instructions to install and activate the web app are in cv_builder/README.md**

## Table of Contents

1. [Description](#description)
2. [Purpose](#purpose)
3. [Features](#features)
4. [Technology Stack](#technology-stack)
5. [System Requirements](#system-requirements)
6. [Installation Instructions](#installation-instructions)
    - [Step-by-Step Guide](#step-by-step-guide)
        - [Clone the repository](#1-clone-the-repository)
        - [Set up a virtual environment](#2-set-up-a-virtual-environment)
        - [Install dependencies](#3-install-dependencies)
        - [Set up the MySQL database](#4-set-up-the-mysql-database)
        - [Configuration](#5-configuration)
        - [Usage](#6-usage)
        - [Development Setup](#7-development-setup)
    - [Contribution Guidelines](#contribution-guidelines)
    - [Contact Information](#contact-information)

---

### 1. Description <a name="description"></a>

LinkedIn Jobs is a project aimed at enhancing the job search experience by scraping job listings from LinkedIn, processing them using the ChatGPT API, and storing them in a MySQL database. The project includes a web application for browsing job listings and generating CVs.

### 2. Purpose <a name="purpose"></a>

The project addresses issues with the LinkedIn job search, such as irrelevant listings and ineffective filters, providing a more efficient and tailored job hunting experience.

### 3. Features <a name="features"></a>

- Web scraper for LinkedIn job listings
- Processing of job listings using ChatGPT API
- Storage of job listings in a MySQL database
- Web application for viewing job listings
- CV generation tool

### 4. Technology Stack <a name="technology-stack"></a>

- **Python**: Web scraper and backend development
- **Flask**: Backend of the web application
- **Flutter and Dart**: Frontend of the web application
- **MySQL**: Database storage

### 5. System Requirements <a name="system-requirements"></a>

No specific system requirements.

### 6. Installation Instructions <a name="installation-instructions"></a>

#### Step-by-Step Guide <a name="step-by-step-guide"></a>

#### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Git](https://git-scm.com/downloads)
- [VS Code](https://code.visualstudio.com/download)
- [Python](https://www.python.org/downloads/)
- [MySql](https://www.mysql.com/downloads/)

#### 1. Clone the repository <a name="1-clone-the-repository"></a>
in your terminal / cmd navigate to the folder you want to clone into and do the following steps :
```bash
git clone https://github.com/SlimanJammal/LinkedInJobs.git

cd LinkedInJobs
```

#### 2. Set up a virtual environment <a name="2-set-up-a-virtual-environment"></a>

```bash
python -m venv venv
```
on unix/linux based machines :
```
source venv/bin/activate 
```
on windows :
```
venv\Scripts\activate
```

#### 3. Install dependencies <a name="3-install-dependencies"></a>

```bash
pip install -r requirements.txt
```

#### 4. Set up a MySQL database <a name="4-set-up-the-mysql-database"></a>

if you don't have Mysql already downloaded you can follow this [tutorial](https://www.youtube.com/watch?v=u96rVINbAUI) or the followin steps:
- [Install MySQL](https://dev.mysql.com/doc/workbench/en/) if not already installed.
- Create a new database.
- Update the database configuration in `credintials.py` with your MySQL credentials.

#### 5. Configuration <a name="5-configuration"></a>

open the `credintials.py` file and update the following (replace the variable values with your information ) :

- MySQL database connection details
- LinkedIn details (we highly suggest to use a temporary account not your main one)

Then add your ChatGPT API key to your environment variables, to do that follow step 2 (Set Up API Key) [here](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key).

#### 6. Usage <a name="6-usage"></a>

1) **Run the scraper to populate the database with job listings.**

```bash
python main.py <FIELD> [OPTION]
```

- `<FIELD>`: Specify the field of interest using one of the following options:
   - `EE` for Electrical Engineering.
   - `CS` for Computer Science.
   - `ME` for Mechanical Engineering.
- `[OPTION]` (Optional):
   - `DB_CREATE`: Use this option to create or update the database. It deletes all existing data and creates new tables.

**Example:**

```bash
python main.py CS DB_CREATE
```

If the database is already created, you can run:

```bash
python main.py CS
```

2) **Start the web application to view job listings and generate CVs.**

**to start the web appliction follow the instructions inside /cv_builder/README.md**

#### 7. Development Setup <a name="7-development-setup"></a>

- Follow the installation instructions to set up the project.
- Make sure to activate the virtual environment before making changes.
- Use proper branching and pull requests for contributions.

### Contribution Guidelines <a name="contribution-guidelines"></a>

1) Fork the repository.
2) Create a new branch (`git checkout -b feature/your-feature-name`).
3) Commit your changes (`git commit -am 'Add some feature'`).
4) Push to the branch (`git push origin feature/your-feature-name`).
5) Create a new Pull Request.

### Contact Information <a name="contact-information"></a>

For support or questions, please contact [Muhammad Eid](https://github.com/Mohammad-Eid) / [Sliman Jammal](https://github.com/SlimanJammal).





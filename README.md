# CampusPlaceAI

## AI-Powered Placement Coordination Platform

CampusPlaceAI is a centralized placement management platform developed using Django and Artificial Intelligence techniques to automate campus recruitment workflows.

The system enables educational institutions, students, and administrators to manage placement activities efficiently through role-based access control, resume analysis, and intelligent job matching.

---

## Project Overview

CampusPlaceAI was developed to address the challenges of traditional campus placement management systems, where recruitment processes are often manual, time-consuming, and difficult to coordinate across multiple institutions.

The platform centralizes placement activities and provides AI-powered features such as resume scoring, placement readiness assessment, and student-job matching.

---

## Key Features

### Institution Management

- Institution registration request workflow
- Admin approval and rejection system
- Automatic institution code generation
- College administrator access control
- Institution-specific student management

### Student Management

- Student profile management
- Resume upload functionality
- Placement readiness tracking
- Profile correction request workflow
- AI-generated resume analysis

### Job Management

- Job posting by system administrator
- Eligibility and branch-based filtering
- Required skills management
- Candidate shortlisting
- Placement selection tracking

### AI Features

#### Resume Scoring Engine

The system evaluates student resumes using heuristic NLP techniques based on:

- Skill keyword identification
- Resume content analysis
- Academic performance
- Backlog consideration
- Placement readiness assessment

Outputs include:

- Resume Score (0–100)
- Readiness Level
- Job Recommendations

#### Intelligent Job Matching

The AI matching engine evaluates:

- Student skills
- Academic qualifications
- Branch eligibility
- CGPA
- Resume readiness

The system automatically ranks candidates and generates a match score for each student.

### Placement Tracking

- Student-job matching
- Selection management
- Placement history tracking
- Selected student management

---

## System Modules

### System Administrator

Responsibilities:

- Approve or reject institution requests
- Generate institution access codes
- Add and manage students
- Post and manage jobs
- View AI-generated candidate matches
- Select students for recruitment drives
- Manage correction requests

### College Administrator

Responsibilities:

- Access institution dashboard
- View institution details
- Monitor student profiles
- View placement results
- Track selected students

### Student

Responsibilities:

- Login using institution code
- Manage profile information
- Upload resume
- View resume score
- View readiness status
- Receive job recommendations
- Submit correction requests

---

## Technology Stack

### Backend

- Python
- Django

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Database

- SQLite

### AI Components

- Python Text Processing
- Heuristic NLP
- Resume Parsing Engine
- Skill-Based Recommendation System
- AI Matching Algorithm

---

## Project Structure

```text
CampusPlaceAI/
│
├── accounts/
├── ai_engine/
│   ├── matcher.py
│   ├── scorer.py
│   ├── resume_parser.py
│   ├── job_recommender.py
│   └── ai_loader.py
│
├── institutions/
├── students/
├── jobs/
├── requests/
├── core/
│
├── templates/
├── static/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## AI Workflow

### Resume Analysis Process

1. Student uploads resume
2. Resume parser extracts text content
3. Skills are identified from resume
4. Resume scoring engine evaluates profile
5. Readiness level is generated
6. Results are stored in database

### Job Matching Process

1. Administrator posts job requirements
2. Required skills are defined
3. AI matching engine evaluates candidates
4. Match score is calculated
5. Students are ranked
6. Administrator selects candidates

---

## Database Entities

### Institution

Stores:

- Institution details
- Institution code
- Approval status

### Student

Stores:

- Personal details
- Academic information
- Skills
- Resume information
- Readiness score

### Job

Stores:

- Company information
- Job details
- Eligibility criteria
- Required skills

### PlacementSelection

Stores:

- Selected student
- Associated job
- Match score
- Selection date

### CollegeRequest

Stores:

- Institution registration requests
- Approval workflow information

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/CampusPlaceAI.git
cd CampusPlaceAI
```

### Create Virtual Environment

```bash
python -m venv campusplaceaienv
```

### Activate Environment

Linux/macOS:

```bash
source campusplaceaienv/bin/activate
```

Windows:

```bash
campusplaceaienv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

---

## Future Enhancements

- Machine Learning based resume scoring
- Advanced NLP resume parser
- Interview scheduling module
- Email notification system
- Placement analytics dashboard
- Real-time placement statistics
- Cloud deployment support
- Multi-company recruitment drives

---

## Academic Project Information

**Project Title:** CampusPlaceAI – AI-Powered Placement Coordination Platform

**Domain:** Artificial Intelligence and Web Application Development

**Framework:** Django

**Database:** SQLite
---

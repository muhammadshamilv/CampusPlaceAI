CampusPlaceAI
AI Powered Placement Coordination Platform

CampusPlaceAI is a centralized placement management platform developed using Django and Artificial Intelligence techniques to automate campus recruitment workflows.

The platform supports multiple educational institutions, intelligent resume evaluation, AI-based job matching, and placement management through role-based access control.

Features
Institution Management
Institution registration request workflow
Admin approval and rejection system
Automatic institution code generation
College administrator access control
Student Management
Student profile management
Resume upload
Placement readiness tracking
Correction request workflow
AI Features
Resume text extraction
Resume scoring engine
Placement readiness prediction
Job recommendation system
AI-based student-job matching
Placement Management
Job posting
Candidate matching
Student shortlisting
Selection tracking
Technology Stack
Backend
Django
Python
Frontend
HTML
CSS
Bootstrap
JavaScript
Database
SQLite
AI Components
Heuristic NLP
Resume Parsing
Rule-Based Recommendation Engine
Project Structure
CampusPlaceAI/
│
├── accounts/
├── institutions/
├── students/
├── jobs/
├── ai_engine/
├── requests/
├── core/
│
├── templates/
├── static/
├── media/
│
├── manage.py
└── requirements.txt
Installation
git clone https://github.com/YOUR_USERNAME/CampusPlaceAI.git

cd CampusPlaceAI

python -m venv venv

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py makemigrations
python manage.py migrate

Create admin:

python manage.py createsuperuser

Run server:

python manage.py runserver
Future Enhancements
Machine Learning Resume Scoring
Interview Scheduling
Placement Analytics Dashboard
Email Notifications
Cloud Deployment

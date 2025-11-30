🧠 Smart Task Analyzer

A Django-powered mini-application that analyzes tasks based on urgency, importance, effort, and dependencies — helping you decide what to work on first.

📌 Table of Contents

Overview

Features

Tech Stack

Project Structure

Scoring Algorithm Explanation

API Endpoints

Frontend Usage

Setup & Installation

Example JSON Input

Future Enhancements

🚀 Overview

The Smart Task Analyzer is a task-prioritization tool that intelligently analyzes a list of tasks using a custom scoring algorithm.
Each task is evaluated by:

Urgency (how soon it’s due)

Importance (1–10 scale)

Effort (estimated hours)

Dependencies (blocked tasks get lower priority)

It then returns:

A sorted list of tasks based on priority

A Top 3 task suggestion list with human-readable explanations

This project demonstrates backend logic, edge-case handling, API creation, and basic frontend interaction.

✨ Features
🔹 Backend (Django)

Custom scoring algorithm

Robust handling of missing/invalid data

Two fully functional API endpoints:

/api/tasks/analyze/ → Score & sort tasks

/api/tasks/suggest/ → Recommend top 3 tasks with explanations

🔹 Frontend (HTML, CSS, JavaScript)

JSON textarea for task input

“Analyze Tasks” & “Suggest Top 3” buttons

Beautiful dark-themed UI

Color-coded priority cards (high/medium/low)

Built-in sorting strategies:

Smart Score (default)

Fastest Wins

Deadline Driven

🛠 Tech Stack

Backend: Django 4+, Python 3.8+
Frontend: HTML, CSS, Vanilla JavaScript
Database: SQLite
Tools: Fetch API, JSON parsing

📁 Project Structure
task-analyzer/
├── backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── models.py
│   ├── scoring.py        ← Core algorithm
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── manage.py
└── db.sqlite3

🧮 Scoring Algorithm Explanation

Each task receives a priority score based on four factors:

1️⃣ Urgency (due_date)
Condition	Score
Overdue	+80
Due today/tomorrow	+60
Due in ≤3 days	+40
Due in ≤7 days	+20
Later	+0
2️⃣ Importance (1–10)
score += importance * 7


Importance is weighted heavily because a task’s significance should strongly influence its priority.

3️⃣ Effort (estimated_hours)
Hours	Bonus
≤1 hr	+20
≤3 hrs	+10
≥8 hrs	-10

Quick tasks receive a “quick win” bonus.

4️⃣ Dependencies
score -= 15


Tasks with dependencies get reduced priority because they might be blocked.

🔌 API Endpoints
📍 1. Analyze Tasks

POST → /api/tasks/analyze/

Input:
A JSON array of tasks.

Output:

Each task with an added score

Sorted by priority (descending)

📍 2. Suggest Top 3 Tasks

POST → /api/tasks/suggest/

Output:
Top 3 prioritized tasks for “today”, with:

Score

Natural language explanation (urgency, importance, effort, blocking status)

💻 Frontend Usage

Run Django server:

python manage.py runserver


Open:

http://127.0.0.1:8000/


Paste JSON into the textarea.

Click:

Analyze Tasks → Score and sort

Suggest Top 3 → Best 3 tasks with explanations

Results appear on the right side as styled cards.

📝 Example JSON Input
[
  {
    "title": "Finish assignment",
    "due_date": "2025-02-05",
    "importance": 9,
    "estimated_hours": 2,
    "dependencies": []
  },
  {
    "title": "Buy groceries",
    "due_date": "2025-02-10",
    "importance": 3,
    "estimated_hours": 1,
    "dependencies": []
  }
]

🧩 Setup & Installation
1️⃣ Clone the repository
git clone <your-repo-url>
cd task-analyzer

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   (Windows)
source venv/bin/activate  (Mac/Linux)

3️⃣ Install dependencies
pip install django

4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Start development server
python manage.py runserver

6️⃣ Open the app
http://127.0.0.1:8000/

🚀 Future Enhancements

Form-based UI (no JSON required)

Persistent task storage in DB

Edit/delete tasks on UI

Add user authentication

Gantt chart or timeline visualization

Machine-learning–based scoring system

🎉 Final Notes

This project showcases:

✔ Backend logic
✔ API development
✔ Scoring & ranking algorithm
✔ Frontend–backend communication
✔ Handling of real-world edge cases
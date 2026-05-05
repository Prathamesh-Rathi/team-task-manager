# TaskFlow — Team Task Manager

A full-stack team task management web application built with Flask, SQLAlchemy, and SQLite.

## Live Demo
🔗 [https://your-railway-url.up.railway.app](https://your-railway-url.up.railway.app)

## Features
- User authentication (signup / login / logout)
- Create and manage projects
- Role-based access (Admin / Member)
- Task board with To Do / In Progress / Done columns
- Assign tasks to team members
- Due dates, priorities, overdue detection
- Dashboard with stats

## Tech Stack
- **Backend:** Flask, SQLAlchemy, Flask-Bcrypt
- **Database:** SQLite (local) / PostgreSQL (production)
- **Frontend:** Jinja2 templates, Bootstrap 5
- **Deployment:** Railway

## Local Setup

### 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/team-task-manager.git
cd team-task-manager

### 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the app
python run.py

### 5. Open in browser
http://127.0.0.1:5000

## Project Structure
team-task-manager/
├── app/
│   ├── __init__.py      # App factory
│   ├── models.py        # Database models
│   ├── auth.py          # Authentication routes
│   ├── projects.py      # Project routes
│   ├── tasks.py         # Task routes
│   ├── dashboard.py     # Dashboard route
│   ├── utils.py         # Helper functions
│   └── templates/       # HTML templates
├── config.py            # Configuration
├── run.py               # Entry point
├── Procfile             # Railway start command
└── requirements.txt     # Dependencies

## Deployment (Railway)
1. Push code to GitHub
2. Connect repo on railway.app
3. Add environment variables (SECRET_KEY, JWT_SECRET_KEY)
4. Generate domain from Settings tab

## Default Roles
- **Admin** — creates project, manages members and tasks
- **Member** — views project, updates task status only

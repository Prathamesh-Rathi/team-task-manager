

# 🚀 TaskFlow — Team Task Manager

A full-stack **team task management web application** built using Flask.
TaskFlow helps teams collaborate efficiently by organizing projects, assigning tasks, and tracking progress in real-time.

---

## 🌐 Live Demo

🔗 [https://team-task-manager-2-g3tk.onrender.com](https://team-task-manager-2-g3tk.onrender.com)

---

## ✨ Key Features

### 🔐 Authentication & Security

* User Signup, Login, Logout
* Password hashing using Flask-Bcrypt
* Secure session management

### 📁 Project Management

* Create and manage multiple projects
* Add/remove team members
* Role-based access control

### 👥 Role-Based Access

* **Admin**

  * Create and manage projects
  * Assign tasks
  * Manage team members
* **Member**

  * View assigned projects
  * Update task status

### 📌 Task Management

* Kanban-style task board:

  * To Do
  * In Progress
  * Done
* Assign tasks to users
* Set priorities and due dates
* Overdue task detection

### 📊 Dashboard & Insights

* Project-level statistics
* Task progress tracking
* Visual overview of workload

---

## 🛠️ Tech Stack

### Backend

* Flask
* SQLAlchemy
* Flask-Bcrypt

### Frontend

* Jinja2 Templates
* Bootstrap 5

### Database

* SQLite (Development)
* PostgreSQL (Production-ready)

### Deployment

* Render (Live Hosting)

---

## ⚙️ Local Setup Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/team-task-manager.git
cd team-task-manager
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application

```bash
python run.py
```

---

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 📂 Project Structure

```
team-task-manager/
│
├── app/
│   ├── __init__.py      # App factory
│   ├── models.py        # Database models
│   ├── auth.py          # Authentication routes
│   ├── projects.py      # Project management
│   ├── tasks.py         # Task management
│   ├── dashboard.py     # Dashboard logic
│   ├── utils.py         # Helper utilities
│   └── templates/       # HTML templates
│
├── config.py            # App configuration
├── run.py               # Application entry point
├── Procfile             # Deployment start command
├── requirements.txt     # Python dependencies
└── .gitignore           # Ignored files
```

---

## 🚀 Deployment Guide (Render)

### Steps to Deploy

1. Push your code to GitHub
2. Go to Render
3. Create a **New Web Service**
4. Connect your repository

### 🔧 Configuration

* **Build Command**

```bash
pip install -r requirements.txt
```

* **Start Command**

```bash
gunicorn run:app
```

---

## 🔐 Environment Variables

Add the following in Render:

| Variable         | Description            |
| ---------------- | ---------------------- |
| `SECRET_KEY`     | Flask secret key       |
| `JWT_SECRET_KEY` | JWT authentication key |
| `FLASK_ENV`      | Set to `production`    |

---

## 👤 Default Roles

### 🛡️ Admin

* Create and manage projects
* Add/remove members
* Assign and manage tasks

### 👨‍💻 Member

* View assigned projects
* Update task status only

---

## 📌 Future Enhancements

* Real-time notifications
* File attachments in tasks
* Activity logs
* REST API integration
* Email reminders

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is open-source and available under the MIT License.



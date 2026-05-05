from flask import Blueprint, render_template, session
from app.models import Project, Task, ProjectMember, User
from app.utils import login_required, get_current_user
from app import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    user = get_current_user()

    # Projects this user belongs to
    memberships = ProjectMember.query.filter_by(user_id=user.id).all()
    project_ids = [m.project_id for m in memberships]
    projects    = Project.query.filter(Project.id.in_(project_ids)).all()

    # All tasks in those projects
    all_tasks = Task.query.filter(Task.project_id.in_(project_ids)).all()

    # Stats
    total_tasks      = len(all_tasks)
    todo_tasks       = [t for t in all_tasks if t.status == 'todo']
    inprogress_tasks = [t for t in all_tasks if t.status == 'in_progress']
    done_tasks       = [t for t in all_tasks if t.status == 'done']
    overdue_tasks    = [t for t in all_tasks if t.is_overdue]

    # My assigned tasks
    my_tasks = Task.query.filter_by(assignee_id=user.id).limit(5).all()

    return render_template('dashboard.html',
        user             = user,
        projects         = projects,
        total_tasks      = total_tasks,
        todo_count       = len(todo_tasks),
        inprogress_count = len(inprogress_tasks),
        done_count       = len(done_tasks),
        overdue_count    = len(overdue_tasks),
        my_tasks         = my_tasks,
        all_tasks        = all_tasks,
    )
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Task, Project, ProjectMember, User
from app.utils import login_required, get_current_user, get_user_role
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)


# ── My tasks ──────────────────────────────────────────
@tasks_bp.route('/tasks')
@login_required
def my_tasks():
    user  = get_current_user()
    tasks = Task.query.filter_by(assignee_id=user.id).order_by(Task.due_date.asc()).all()
    return render_template('tasks/my_tasks.html', tasks=tasks, user=user)


# ── Create task ───────────────────────────────────────
@tasks_bp.route('/projects/<int:project_id>/tasks/new', methods=['GET', 'POST'])
@login_required
def create_task(project_id):
    user    = get_current_user()
    project = Project.query.get_or_404(project_id)
    role    = get_user_role(project_id)

    if not role:
        flash('Access denied.', 'danger')
        return redirect(url_for('projects.list_projects'))

    if role != 'admin':
        flash('Only admins can create tasks.', 'danger')
        return redirect(url_for('projects.project_detail', project_id=project_id))

    members = (
        db.session.query(User)
        .join(ProjectMember, ProjectMember.user_id == User.id)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )

    if request.method == 'POST':
        title       = request.form.get('title',       '').strip()
        description = request.form.get('description', '').strip()
        due_date_s  = request.form.get('due_date',    '').strip()
        priority    = request.form.get('priority',    'medium')
        assignee_id = request.form.get('assignee_id', type=int)

        if not title:
            flash('Task title is required.', 'danger')
            return render_template('tasks/create.html', project=project, members=members)

        due_date = None
        if due_date_s:
            try:
                due_date = datetime.strptime(due_date_s, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format.', 'danger')
                return render_template('tasks/create.html', project=project, members=members)

        task = Task(
            title       = title,
            description = description,
            due_date    = due_date,
            priority    = priority,
            assignee_id = assignee_id or None,
            creator_id  = user.id,
            project_id  = project_id,
            status      = 'todo',
        )
        db.session.add(task)
        db.session.commit()

        flash(f'Task "{title}" created!', 'success')
        return redirect(url_for('projects.project_detail', project_id=project_id))

    return render_template('tasks/create.html', project=project, members=members)


# ── Edit / update task ────────────────────────────────
@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    user = get_current_user()
    task = Task.query.get_or_404(task_id)
    role = get_user_role(task.project_id)

    if not role:
        flash('Access denied.', 'danger')
        return redirect(url_for('projects.list_projects'))

    project = Project.query.get(task.project_id)
    members = (
        db.session.query(User)
        .join(ProjectMember, ProjectMember.user_id == User.id)
        .filter(ProjectMember.project_id == task.project_id)
        .all()
    )

    if request.method == 'POST':
        # Admins can edit everything; members can only update status
        if role == 'admin':
            task.title       = request.form.get('title',       task.title).strip()
            task.description = request.form.get('description', task.description).strip()
            task.priority    = request.form.get('priority',    task.priority)
            task.assignee_id = request.form.get('assignee_id', type=int) or None
            due_date_s       = request.form.get('due_date', '')
            if due_date_s:
                try:
                    task.due_date = datetime.strptime(due_date_s, '%Y-%m-%d')
                except ValueError:
                    flash('Invalid date.', 'danger')
                    return render_template('tasks/edit.html', task=task, project=project, members=members, role=role)

        # Both admin and member can update status
        new_status = request.form.get('status')
        if new_status in ('todo', 'in_progress', 'done'):
            task.status = new_status

        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('projects.project_detail', project_id=task.project_id))

    return render_template('tasks/edit.html', task=task, project=project, members=members, role=role)


# ── Delete task (Admin only) ──────────────────────────
@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    role = get_user_role(task.project_id)

    if role != 'admin':
        flash('Only admins can delete tasks.', 'danger')
        return redirect(url_for('projects.project_detail', project_id=task.project_id))

    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'success')
    return redirect(url_for('projects.project_detail', project_id=project_id))


# ── Quick status update (AJAX-friendly POST) ──────────
@tasks_bp.route('/tasks/<int:task_id>/status', methods=['POST'])
@login_required
def update_status(task_id):
    task   = Task.query.get_or_404(task_id)
    role   = get_user_role(task.project_id)
    status = request.form.get('status')

    if not role:
        flash('Access denied.', 'danger')
        return redirect(url_for('projects.list_projects'))

    if status in ('todo', 'in_progress', 'done'):
        task.status     = status
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Status updated.', 'success')

    return redirect(url_for('projects.project_detail', project_id=task.project_id))
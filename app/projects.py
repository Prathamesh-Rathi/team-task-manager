from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Project, ProjectMember, User, Task
from app.utils import login_required, get_current_user, get_user_role

projects_bp = Blueprint('projects', __name__)


# ── List all projects for current user ──────────────
@projects_bp.route('/projects')
@login_required
def list_projects():
    user = get_current_user()
    memberships = ProjectMember.query.filter_by(user_id=user.id).all()
    project_ids = [m.project_id for m in memberships]
    projects    = Project.query.filter(Project.id.in_(project_ids)).all()

    # Attach role and task count to each project
    project_data = []
    for p in projects:
        role       = get_user_role(p.id)
        task_count = Task.query.filter_by(project_id=p.id).count()
        member_count = ProjectMember.query.filter_by(project_id=p.id).count()
        project_data.append({
            'project':      p,
            'role':         role,
            'task_count':   task_count,
            'member_count': member_count,
        })

    return render_template('projects/list.html', project_data=project_data)


# ── Create project ───────────────────────────────────
@projects_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def create_project():
    user = get_current_user()

    if request.method == 'POST':
        name        = request.form.get('name',        '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            flash('Project name is required.', 'danger')
            return render_template('projects/create.html')

        project = Project(name=name, description=description, created_by=user.id)
        db.session.add(project)
        db.session.flush()   # get project.id before commit

        # Creator becomes Admin automatically
        membership = ProjectMember(project_id=project.id, user_id=user.id, role='admin')
        db.session.add(membership)
        db.session.commit()

        flash(f'Project "{name}" created!', 'success')
        return redirect(url_for('projects.project_detail', project_id=project.id))

    return render_template('projects/create.html')


# ── Project detail ────────────────────────────────────
@projects_bp.route('/projects/<int:project_id>')
@login_required
def project_detail(project_id):
    user    = get_current_user()
    project = Project.query.get_or_404(project_id)
    role    = get_user_role(project_id)

    if not role:
        flash('You do not have access to this project.', 'danger')
        return redirect(url_for('projects.list_projects'))

    members = (
        db.session.query(ProjectMember, User)
        .join(User, ProjectMember.user_id == User.id)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )

    tasks = Task.query.filter_by(project_id=project_id).all()
    todo_tasks       = [t for t in tasks if t.status == 'todo']
    inprogress_tasks = [t for t in tasks if t.status == 'in_progress']
    done_tasks       = [t for t in tasks if t.status == 'done']

    all_users = User.query.all()

    return render_template('projects/detail.html',
        project          = project,
        role             = role,
        members          = members,
        tasks            = tasks,
        todo_tasks       = todo_tasks,
        inprogress_tasks = inprogress_tasks,
        done_tasks       = done_tasks,
        all_users        = all_users,
        user             = user,
    )


# ── Add member (Admin only) ───────────────────────────
@projects_bp.route('/projects/<int:project_id>/add-member', methods=['POST'])
@login_required
def add_member(project_id):
    role = get_user_role(project_id)
    if role != 'admin':
        flash('Only admins can add members.', 'danger')
        return redirect(url_for('projects.project_detail', project_id=project_id))

    user_id  = request.form.get('user_id',  type=int)
    new_role = request.form.get('role', 'member')

    if not user_id:
        flash('Please select a user.', 'danger')
        return redirect(url_for('projects.project_detail', project_id=project_id))

    existing = ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first()
    if existing:
        flash('User is already a member.', 'warning')
        return redirect(url_for('projects.project_detail', project_id=project_id))

    member = ProjectMember(project_id=project_id, user_id=user_id, role=new_role)
    db.session.add(member)
    db.session.commit()

    user = User.query.get(user_id)
    flash(f'{user.name} added as {new_role}.', 'success')
    return redirect(url_for('projects.project_detail', project_id=project_id))


# ── Remove member (Admin only) ────────────────────────
@projects_bp.route('/projects/<int:project_id>/remove-member/<int:user_id>', methods=['POST'])
@login_required
def remove_member(project_id, user_id):
    current_user = get_current_user()
    role = get_user_role(project_id)

    if role != 'admin':
        flash('Only admins can remove members.', 'danger')
        return redirect(url_for('projects.project_detail', project_id=project_id))

    if user_id == current_user.id:
        flash('You cannot remove yourself.', 'warning')
        return redirect(url_for('projects.project_detail', project_id=project_id))

    membership = ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first()
    if membership:
        db.session.delete(membership)
        db.session.commit()
        flash('Member removed.', 'success')

    return redirect(url_for('projects.project_detail', project_id=project_id))


# ── Delete project (Admin only) ───────────────────────
@projects_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    role = get_user_role(project_id)
    if role != 'admin':
        flash('Only admins can delete projects.', 'danger')
        return redirect(url_for('projects.list_projects'))

    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'success')
    return redirect(url_for('projects.list_projects'))
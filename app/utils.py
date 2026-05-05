from functools import wraps
from flask import session, redirect, url_for, flash
from app.models import User, ProjectMember


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    """Return the logged-in User object, or None."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


def get_user_role(project_id):
    """Return 'admin' | 'member' | None for current user in a project."""
    user = get_current_user()
    if not user:
        return None
    membership = ProjectMember.query.filter_by(
        project_id=project_id,
        user_id=user.id
    ).first()
    return membership.role if membership else None
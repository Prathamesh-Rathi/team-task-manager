from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__)


# ── Signup ──────────────────────────────────────
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name     = request.form.get('name',     '').strip()
        email    = request.form.get('email',    '').strip().lower()
        password = request.form.get('password', '').strip()

        # Validation
        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('auth/signup.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'danger')
            return render_template('auth/signup.html')

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


# ── Login ────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email',    '').strip().lower()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Both fields are required.', 'danger')
            return render_template('auth/login.html')

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html')

        # Store user info in Flask session
        session['user_id']   = user.id
        session['user_name'] = user.name
        session['user_email']= user.email

        flash(f'Welcome back, {user.name}!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html')


# ── Logout ───────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'

    # Railway provides DATABASE_URL automatically if you add a Postgres plugin
    # For now we use SQLite as fallback (works fine for submission)
    raw_db_url = os.environ.get('DATABASE_URL', 'sqlite:///taskmanager.db')

    # Fix for older Railway Postgres URLs that start with postgres:// instead of postgresql://
    if raw_db_url.startswith('postgres://'):
        raw_db_url = raw_db_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = raw_db_url
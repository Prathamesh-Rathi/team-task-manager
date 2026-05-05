from app import create_app, db
from app.models import User, Project, ProjectMember, Task
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ All tables created successfully!")

    inspector = inspect(db.engine)
    print("Tables:", inspector.get_table_names())
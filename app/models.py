from app import db
from datetime import datetime


# ──────────────────────────────────────────
# User Table
# ──────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    project_memberships = db.relationship('ProjectMember', back_populates='user', cascade='all, delete-orphan')
    assigned_tasks      = db.relationship('Task', foreign_keys='Task.assignee_id', back_populates='assignee')
    created_tasks       = db.relationship('Task', foreign_keys='Task.creator_id',  back_populates='creator')

    def to_dict(self):
        return {
            'id':         self.id,
            'name':       self.name,
            'email':      self.email,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.email}>'


# ──────────────────────────────────────────
# Project Table
# ──────────────────────────────────────────
class Project(db.Model):
    __tablename__ = 'projects'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default='')
    created_by  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    members = db.relationship('ProjectMember', back_populates='project', cascade='all, delete-orphan')
    tasks   = db.relationship('Task',          back_populates='project',  cascade='all, delete-orphan')
    creator = db.relationship('User', foreign_keys=[created_by])

    def to_dict(self):
        return {
            'id':          self.id,
            'name':        self.name,
            'description': self.description,
            'created_by':  self.created_by,
            'created_at':  self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Project {self.name}>'


# ──────────────────────────────────────────
# ProjectMember Table  (join table with role)
# ──────────────────────────────────────────
class ProjectMember(db.Model):
    __tablename__ = 'project_members'

    id         = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    role       = db.Column(db.String(20), default='member')   # 'admin' or 'member'
    joined_at  = db.Column(db.DateTime,  default=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', back_populates='members')
    user    = db.relationship('User',    back_populates='project_memberships')

    # One user can only appear once per project
    __table_args__ = (
        db.UniqueConstraint('project_id', 'user_id', name='uq_project_user'),
    )

    def to_dict(self):
        return {
            'id':         self.id,
            'project_id': self.project_id,
            'user_id':    self.user_id,
            'role':       self.role,
            'joined_at':  self.joined_at.isoformat()
        }

    def __repr__(self):
        return f'<ProjectMember project={self.project_id} user={self.user_id} role={self.role}>'


# ──────────────────────────────────────────
# Task Table
# ──────────────────────────────────────────
class Task(db.Model):
    __tablename__ = 'tasks'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        default='')
    due_date    = db.Column(db.DateTime,    nullable=True)
    priority    = db.Column(db.String(20),  default='medium')   # 'low' | 'medium' | 'high'
    status      = db.Column(db.String(30),  default='todo')     # 'todo' | 'in_progress' | 'done'
    project_id  = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=True)
    creator_id  = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project  = db.relationship('Project', back_populates='tasks')
    assignee = db.relationship('User', foreign_keys=[assignee_id], back_populates='assigned_tasks')
    creator  = db.relationship('User', foreign_keys=[creator_id],  back_populates='created_tasks')

    @property
    def is_overdue(self):
        if self.due_date and self.status != 'done':
            return datetime.utcnow() > self.due_date
        return False

    def to_dict(self):
        return {
            'id':            self.id,
            'title':         self.title,
            'description':   self.description,
            'due_date':      self.due_date.isoformat() if self.due_date else None,
            'priority':      self.priority,
            'status':        self.status,
            'project_id':    self.project_id,
            'assignee_id':   self.assignee_id,
            'assignee_name': self.assignee.name if self.assignee else None,
            'creator_id':    self.creator_id,
            'creator_name':  self.creator.name  if self.creator  else None,
            'is_overdue':    self.is_overdue,
            'created_at':    self.created_at.isoformat(),
            'updated_at':    self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Task {self.title} [{self.status}]>'
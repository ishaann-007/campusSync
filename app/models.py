from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'faculty', 'staff', 'management'
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)

    department = db.relationship('Department', backref=db.backref('staff_members', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Issue(db.Model):
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    room_number = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Submitted')
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    submitter = db.relationship('User', foreign_keys=[submitted_by], backref=db.backref('submitted_issues', lazy=True))
    department = db.relationship('Department', backref=db.backref('issues', lazy=True))


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), unique=True, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    issue = db.relationship('Issue', backref=db.backref('assignment', uselist=False))
    staff = db.relationship('User', foreign_keys=[staff_id], backref=db.backref('assignments', lazy=True))

from functools import wraps
from flask import g, redirect, url_for, session, flash
from app import db
from app.models import User

def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user is None:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if g.user.role not in roles:
                flash('Unauthorized access.', 'danger')
                # Redirect to user's own role page if available
                if g.user.role == 'faculty':
                    return redirect(url_for('routes.faculty_dashboard'))
                elif g.user.role == 'staff':
                    return redirect(url_for('routes.staff_placeholder'))
                elif g.user.role == 'management':
                    return redirect(url_for('routes.management_placeholder'))
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

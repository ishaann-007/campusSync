from flask import Blueprint, render_template, redirect, url_for, request, session, flash, g
from app.models import User
from app.auth import login_required

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None:
        if g.user.role == 'faculty':
            return redirect(url_for('routes.faculty_dashboard'))
        elif g.user.role == 'staff':
            return redirect(url_for('routes.staff_dashboard'))
        elif g.user.role == 'management':
            return redirect(url_for('routes.management_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            error = 'Invalid email or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            if user.role == 'faculty':
                return redirect(url_for('routes.faculty_dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('routes.staff_dashboard'))
            elif user.role == 'management':
                return redirect(url_for('routes.management_dashboard'))
            return redirect(url_for('auth.login'))

        flash(error, 'danger')

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

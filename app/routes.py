from flask import Blueprint, render_template, g, redirect, url_for
from app.auth import role_required

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    if g.user:
        if g.user.role == 'faculty':
            return redirect(url_for('routes.faculty_placeholder'))
        elif g.user.role == 'staff':
            return redirect(url_for('routes.staff_placeholder'))
        elif g.user.role == 'management':
            return redirect(url_for('routes.management_placeholder'))
    return redirect(url_for('auth.login'))

@bp.route('/faculty')
@role_required('faculty')
def faculty_placeholder():
    return render_template('faculty/placeholder.html')

@bp.route('/staff')
@role_required('staff')
def staff_placeholder():
    return render_template('staff/placeholder.html')

@bp.route('/management')
@role_required('management')
def management_placeholder():
    return render_template('management/placeholder.html')

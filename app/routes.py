from flask import Blueprint, render_template, g, redirect, url_for, request, flash, abort
from app import db
from app.models import Issue
from app.auth import role_required

bp = Blueprint('routes', __name__)

CATEGORIES = [
    'IT / Equipment',
    'Facilities / Classroom',
    'Academic / Schedule',
    'Miscellaneous'
]

@bp.route('/')
def index():
    if g.user:
        if g.user.role == 'faculty':
            return redirect(url_for('routes.faculty_dashboard'))
        elif g.user.role == 'staff':
            return redirect(url_for('routes.staff_placeholder'))
        elif g.user.role == 'management':
            return redirect(url_for('routes.management_placeholder'))
    return redirect(url_for('auth.login'))

@bp.route('/faculty')
@role_required('faculty')
def faculty_dashboard():
    issues = Issue.query.filter_by(submitted_by=g.user.id).order_by(Issue.created_at.desc()).all()
    selected_issue_id = request.args.get('issue_id', type=int)
    selected_issue = None
    if selected_issue_id:
        issue = Issue.query.get(selected_issue_id)
        if issue and issue.submitted_by == g.user.id:
            selected_issue = issue
        else:
            flash('Issue not found or unauthorized.', 'danger')

    return render_template('faculty/dashboard.html', issues=issues, selected_issue=selected_issue)

@bp.route('/faculty/submit', methods=['GET', 'POST'])
@role_required('faculty')
def faculty_submit_issue():
    if request.method == 'POST':
        problem = request.form.get('problem', '').strip()
        description = request.form.get('description', '').strip()
        room_number = request.form.get('room_number', '').strip()
        category = request.form.get('category', '').strip()

        if not problem or not room_number or not category:
            flash('Problem, Room Number, and Category are required.', 'danger')
            return render_template('faculty/submit.html', categories=CATEGORIES,
                                   problem=problem, description=description, room_number=room_number, category=category)

        if category not in CATEGORIES:
            flash('Invalid category selected.', 'danger')
            return render_template('faculty/submit.html', categories=CATEGORIES,
                                   problem=problem, description=description, room_number=room_number, category=category)

        new_issue = Issue(
            problem=problem,
            description=description,
            room_number=room_number,
            category=category,
            status='Submitted',
            submitted_by=g.user.id
        )

        db.session.add(new_issue)
        db.session.commit()

        flash('Issue submitted successfully.', 'success')
        return redirect(url_for('routes.faculty_dashboard'))

    return render_template('faculty/submit.html', categories=CATEGORIES)

@bp.route('/faculty/issue/<int:issue_id>')
@role_required('faculty')
def faculty_issue_detail(issue_id):
    issue = db.session.get(Issue, issue_id)
    if not issue or issue.submitted_by != g.user.id:
        abort(404)
    return render_template('faculty/detail.html', issue=issue)

@bp.route('/staff')
@role_required('staff')
def staff_placeholder():
    return render_template('staff/placeholder.html')

@bp.route('/management')
@role_required('management')
def management_placeholder():
    return render_template('management/placeholder.html')


from app import db
from app.models import Department, User, Issue, Assignment

# Category to Department name mapping per specification
CATEGORY_DEPARTMENT_MAP = {
    'IT / Equipment': 'IT Department',
    'Facilities / Classroom': 'Facilities Department',
    'Academic / Schedule': 'Academic Administration',
    'Miscellaneous': 'General Administration'
}

def get_department_for_category(category):
    """
    Determines and returns the Department instance corresponding to the given issue category.
    Returns None if category is unmapped or department is not found in database.
    """
    dept_name = CATEGORY_DEPARTMENT_MAP.get(category)
    if not dept_name:
        return None
    return Department.query.filter_by(name=dept_name).first()

def assign_issue_to_staff(issue):
    """
    Automatically assigns a routed issue to an eligible Staff member based on active workload.
    - Eligible: User.role == 'staff' and User.department_id == issue.department_id
    - Active workload: Count of assigned issues with status 'Assigned' or 'In Progress'
    - Selection: Lowest active workload.
    - Tie-breaker: Alphabetical order by staff name.
    - Result: Creates Assignment, sets Issue status to 'Assigned'.
    - If no eligible staff: No Assignment created, Issue status remains 'Submitted'.
    """
    if not issue or not issue.department_id:
        return None

    eligible_staff = User.query.filter_by(
        role='staff',
        department_id=issue.department_id
    ).all()

    if not eligible_staff:
        return None

    # Calculate active workload for each eligible staff member
    staff_workloads = []
    for staff in eligible_staff:
        workload = db.session.query(Assignment).join(Issue).filter(
            Assignment.staff_id == staff.id,
            Issue.status.in_(['Assigned', 'In Progress'])
        ).count()
        staff_workloads.append((workload, staff.name, staff))

    # Sort by workload ascending, then by staff name ascending (alphabetical)
    staff_workloads.sort(key=lambda x: (x[0], x[1]))

    selected_staff = staff_workloads[0][2]

    # Create assignment record and update issue status
    assignment = Assignment(
        issue_id=issue.id,
        staff_id=selected_staff.id
    )
    issue.status = 'Assigned'

    db.session.add(assignment)
    db.session.commit()

    return assignment


from app import db
from app.models import Department

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

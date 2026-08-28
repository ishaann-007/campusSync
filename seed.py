from app import create_app, db
from app.models import User, Department

def seed_data():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Seed Departments
        dept_names = [
            'IT Department',
            'Facilities Department',
            'Academic Administration',
            'General Administration'
        ]
        departments = {}
        for name in dept_names:
            dept = Department.query.filter_by(name=name).first()
            if not dept:
                dept = Department(name=name)
                db.session.add(dept)
            departments[name] = dept
        
        db.session.commit()

        # Pre-created users according to research.md & architecture.md
        users_to_create = [
            {
                'name': 'Faculty Member 1',
                'email': 'faculty@campussync.edu',
                'password': 'password123',
                'role': 'faculty',
                'department': None
            },
            {
                'name': 'Staff Member IT',
                'email': 'staff.it@campussync.edu',
                'password': 'password123',
                'role': 'staff',
                'department': departments['IT Department']
            },
            {
                'name': 'Staff Member Facilities',
                'email': 'staff.facilities@campussync.edu',
                'password': 'password123',
                'role': 'staff',
                'department': departments['Facilities Department']
            },
            {
                'name': 'Management User',
                'email': 'management@campussync.edu',
                'password': 'password123',
                'role': 'management',
                'department': None
            }
        ]

        for u in users_to_create:
            user = User.query.filter_by(email=u['email']).first()
            if not user:
                user = User(
                    name=u['name'],
                    email=u['email'],
                    role=u['role'],
                    department_id=u['department'].id if u['department'] else None
                )
                user.set_password(u['password'])
                db.session.add(user)

        db.session.commit()
        print("Pre-created seed users successfully initialized.")

if __name__ == '__main__':
    seed_data()

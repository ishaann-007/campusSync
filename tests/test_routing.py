import unittest
from app import create_app, db
from app.models import User, Department, Issue

class DepartmentRoutingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SECRET_KEY': 'test_secret',
            'WTF_CSRF_ENABLED': False
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

            # Seed standard departments
            d_it = Department(name='IT Department')
            d_fac = Department(name='Facilities Department')
            d_acad = Department(name='Academic Administration')
            d_gen = Department(name='General Administration')

            db.session.add_all([d_it, d_fac, d_acad, d_gen])
            db.session.commit()

            # Create test faculty member
            f = User(name='Faculty User', email='faculty@test.com', role='faculty')
            f.set_password('pass123')
            db.session.add(f)
            db.session.commit()

            self.f_id = f.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def login(self, email='faculty@test.com', password='pass123'):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_it_equipment_category_routes_to_it_department(self):
        self.login()
        self.client.post('/faculty/submit', data=dict(
            problem='Projector broken',
            description='Bulb is flickering',
            room_number='Room 101',
            category='IT / Equipment'
        ), follow_redirects=True)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Projector broken').first()
            self.assertIsNotNone(issue)
            self.assertIsNotNone(issue.department_id)
            self.assertEqual(issue.department.name, 'IT Department')
            self.assertEqual(issue.status, 'Submitted')

    def test_facilities_classroom_category_routes_to_facilities_department(self):
        self.login()
        self.client.post('/faculty/submit', data=dict(
            problem='Broken AC',
            description='Room is too hot',
            room_number='Room 202',
            category='Facilities / Classroom'
        ), follow_redirects=True)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Broken AC').first()
            self.assertIsNotNone(issue)
            self.assertIsNotNone(issue.department_id)
            self.assertEqual(issue.department.name, 'Facilities Department')

    def test_academic_schedule_category_routes_to_academic_administration(self):
        self.login()
        self.client.post('/faculty/submit', data=dict(
            problem='Schedule overlap',
            description='Double booking',
            room_number='Room 303',
            category='Academic / Schedule'
        ), follow_redirects=True)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Schedule overlap').first()
            self.assertIsNotNone(issue)
            self.assertIsNotNone(issue.department_id)
            self.assertEqual(issue.department.name, 'Academic Administration')

    def test_miscellaneous_category_routes_to_general_administration(self):
        self.login()
        self.client.post('/faculty/submit', data=dict(
            problem='Lost key card',
            description='Lost key card near cafeteria',
            room_number='Main Hall',
            category='Miscellaneous'
        ), follow_redirects=True)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Lost key card').first()
            self.assertIsNotNone(issue)
            self.assertIsNotNone(issue.department_id)
            self.assertEqual(issue.department.name, 'General Administration')

    def test_faculty_cannot_override_department(self):
        self.login()
        # Attempt to pass a malicious/spoofed department_id parameter in form
        self.client.post('/faculty/submit', data=dict(
            problem='Attempt department override',
            description='Testing override prevention',
            room_number='Room 404',
            category='IT / Equipment',
            department_id=999
        ), follow_redirects=True)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Attempt department override').first()
            self.assertIsNotNone(issue)
            self.assertIsNotNone(issue.department_id)
            # Must route to IT Department regardless of any department_id form submission
            self.assertEqual(issue.department.name, 'IT Department')

if __name__ == '__main__':
    unittest.main()

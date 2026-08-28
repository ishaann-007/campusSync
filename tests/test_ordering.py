import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Department, Issue, Assignment

class IssueOrderingTestCase(unittest.TestCase):
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

            dept = Department(name='IT Department')
            db.session.add(dept)
            db.session.commit()

            f = User(name='Faculty User', email='faculty@test.com', role='faculty')
            f.set_password('pass123')
            
            s = User(name='Staff User', email='staff@test.com', role='staff', department_id=dept.id)
            s.set_password('pass123')

            db.session.add_all([f, s])
            db.session.commit()

            self.f_id = f.id
            self.s_id = s.id

            now = datetime.utcnow()

            # Active Issues
            i1 = Issue(problem='Active Oldest (#1)', room_number='101', category='IT / Equipment', status='Submitted', submitted_by=self.f_id, created_at=now - timedelta(hours=5))
            i2 = Issue(problem='Active Mid (#2)', room_number='102', category='IT / Equipment', status='In Progress', submitted_by=self.f_id, created_at=now - timedelta(hours=3))
            i3 = Issue(problem='Active Newest (#3)', room_number='103', category='IT / Equipment', status='Assigned', submitted_by=self.f_id, created_at=now - timedelta(hours=1))

            # Resolved Issues
            i4 = Issue(problem='Resolved Older (#4)', room_number='104', category='IT / Equipment', status='Resolved', submitted_by=self.f_id, created_at=now - timedelta(hours=4))
            i5 = Issue(problem='Resolved Newest (#5)', room_number='105', category='IT / Equipment', status='Resolved', submitted_by=self.f_id, created_at=now - timedelta(hours=2))

            db.session.add_all([i1, i2, i3, i4, i5])
            db.session.commit()

            # Assignments for staff
            for iss in [i1, i2, i3, i4, i5]:
                asg = Assignment(issue_id=iss.id, staff_id=self.s_id)
                db.session.add(asg)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def login(self, email='faculty@test.com', password='pass123'):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_faculty_dashboard_issue_ordering(self):
        self.login('faculty@test.com')
        response = self.client.get('/faculty')
        self.assertEqual(response.status_code, 200)

        # Expected order: #3 (Active Newest), #2 (Active Mid), #1 (Active Oldest), #5 (Resolved Newest), #4 (Resolved Older)
        p3 = response.data.find(b'Active Newest (#3)')
        p2 = response.data.find(b'Active Mid (#2)')
        p1 = response.data.find(b'Active Oldest (#1)')
        p5 = response.data.find(b'Resolved Newest (#5)')
        p4 = response.data.find(b'Resolved Older (#4)')

        self.assertTrue(p3 < p2 < p1 < p5 < p4, f"Order failed: p3={p3}, p2={p2}, p1={p1}, p5={p5}, p4={p4}")

    def test_staff_dashboard_issue_ordering(self):
        self.login('staff@test.com')
        response = self.client.get('/staff')
        self.assertEqual(response.status_code, 200)

        p3 = response.data.find(b'Active Newest (#3)')
        p2 = response.data.find(b'Active Mid (#2)')
        p1 = response.data.find(b'Active Oldest (#1)')
        p5 = response.data.find(b'Resolved Newest (#5)')
        p4 = response.data.find(b'Resolved Older (#4)')

        self.assertTrue(p3 < p2 < p1 < p5 < p4, f"Order failed: p3={p3}, p2={p2}, p1={p1}, p5={p5}, p4={p4}")

if __name__ == '__main__':
    unittest.main()

import unittest
from app import create_app, db
from app.models import User, Department, Issue

class FacultyIssueSubmissionTestCase(unittest.TestCase):
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

            # Create test faculty members
            f1 = User(name='Faculty One', email='f1@test.com', role='faculty')
            f1.set_password('pass123')

            f2 = User(name='Faculty Two', email='f2@test.com', role='faculty')
            f2.set_password('pass123')

            # Create staff and management
            staff = User(name='Staff Member', email='staff@test.com', role='staff')
            staff.set_password('pass123')

            mgmt = User(name='Management Member', email='mgmt@test.com', role='pass123', role_name='management') if hasattr(User, 'role_name') else User(name='Management Member', email='mgmt@test.com', role='management')
            mgmt.set_password('pass123')

            db.session.add_all([f1, f2, staff, mgmt])
            db.session.commit()

            self.f1_id = f1.id
            self.f2_id = f2.id
            self.staff_id = staff.id
            self.mgmt_id = mgmt.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def login(self, email, password='pass123'):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_authenticated_faculty_can_submit_valid_issue(self):
        self.login('f1@test.com')
        response = self.client.post('/faculty/submit', data=dict(
            problem='Projector broken',
            description='Bulb is flickering and shuts off',
            room_number='Room 204',
            category='IT / Equipment'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Issue submitted successfully', response.data)
        self.assertIn(b'Projector broken', response.data)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Projector broken').first()
            self.assertIsNotNone(issue)
            self.assertEqual(issue.submitted_by, self.f1_id)
            self.assertEqual(issue.status, 'Submitted')
            self.assertEqual(issue.room_number, 'Room 204')
            self.assertEqual(issue.category, 'IT / Equipment')
            self.assertIsNotNone(issue.created_at)
            self.assertIsNone(issue.resolved_at)

    def test_required_field_validation_rejects_invalid_submissions(self):
        self.login('f1@test.com')

        # Missing problem
        response = self.client.post('/faculty/submit', data=dict(
            problem='',
            description='Test desc',
            room_number='Room 101',
            category='IT / Equipment'
        ), follow_redirects=True)
        self.assertIn(b'Problem, Room Number, and Category are required', response.data)

        # Missing room number
        response = self.client.post('/faculty/submit', data=dict(
            problem='Broken AC',
            description='Test desc',
            room_number='',
            category='Facilities / Classroom'
        ), follow_redirects=True)
        self.assertIn(b'Problem, Room Number, and Category are required', response.data)

        # Invalid category
        response = self.client.post('/faculty/submit', data=dict(
            problem='Broken AC',
            description='Test desc',
            room_number='Room 101',
            category='NonExistentCategory'
        ), follow_redirects=True)
        self.assertIn(b'Invalid category selected', response.data)

        with self.app.app_context():
            count = Issue.query.count()
            self.assertEqual(count, 0)

    def test_unauthenticated_user_cannot_submit_issue(self):
        response = self.client.post('/faculty/submit', data=dict(
            problem='Test problem',
            room_number='101',
            category='IT / Equipment'
        ), follow_redirects=True)

        self.assertIn(b'Please log in to access this page', response.data)
        with self.app.app_context():
            self.assertEqual(Issue.query.count(), 0)

    def test_non_faculty_role_cannot_submit_issue(self):
        self.login('staff@test.com')
        response = self.client.post('/faculty/submit', data=dict(
            problem='Staff submitting',
            room_number='101',
            category='IT / Equipment'
        ), follow_redirects=True)

        self.assertIn(b'Unauthorized access', response.data)
        with self.app.app_context():
            self.assertEqual(Issue.query.count(), 0)

    def test_faculty_isolation_of_issues_and_details(self):
        # f1 submits issue
        self.login('f1@test.com')
        self.client.post('/faculty/submit', data=dict(
            problem='Faculty 1 issue',
            room_number='101',
            category='IT / Equipment'
        ))
        self.logout()

        # f2 submits issue
        self.login('f2@test.com')
        self.client.post('/faculty/submit', data=dict(
            problem='Faculty 2 issue',
            room_number='202',
            category='Facilities / Classroom'
        ))

        # f2 views dashboard
        response = self.client.get('/faculty')
        self.assertIn(b'Faculty 2 issue', response.data)
        self.assertNotIn(b'Faculty 1 issue', response.data)

        with self.app.app_context():
            f1_issue = Issue.query.filter_by(problem='Faculty 1 issue').first()
            f2_issue = Issue.query.filter_by(problem='Faculty 2 issue').first()

            f1_issue_id = f1_issue.id
            f2_issue_id = f2_issue.id

        # f2 views own issue detail -> 200
        resp_own = self.client.get(f'/faculty/issue/{f2_issue_id}')
        self.assertEqual(resp_own.status_code, 200)
        self.assertIn(b'Faculty 2 issue', resp_own.data)

        # f2 attempts to view f1 issue detail -> 404
        resp_other = self.client.get(f'/faculty/issue/{f1_issue_id}')
        self.assertEqual(resp_other.status_code, 404)

    def test_submitted_issue_details_cannot_be_edited(self):
        self.login('f1@test.com')
        self.client.post('/faculty/submit', data=dict(
            problem='Immutable problem',
            room_number='101',
            category='IT / Equipment'
        ))

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Immutable problem').first()
            issue_id = issue.id

        # Check detail page rendering (read-only view, no form inputs for editing problem/category/status)
        response = self.client.get(f'/faculty/issue/{issue_id}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'<form', response.data)
        self.assertNotIn(b'name="problem"', response.data)

if __name__ == '__main__':
    unittest.main()

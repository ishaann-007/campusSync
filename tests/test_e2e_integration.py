import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Department, Issue, Assignment

class EndToEndIntegrationTestCase(unittest.TestCase):
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

            # Create Departments
            dept_it = Department(name='IT Department')
            dept_fac = Department(name='Facilities Department')
            dept_acad = Department(name='Academic Administration')
            dept_gen = Department(name='General Administration')

            db.session.add_all([dept_it, dept_fac, dept_acad, dept_gen])
            db.session.commit()

            self.dept_it_id = dept_it.id
            self.dept_fac_id = dept_fac.id

            # Create Users
            faculty1 = User(name='Faculty One', email='faculty1@test.com', role='faculty')
            faculty1.set_password('pass123')

            faculty2 = User(name='Faculty Two', email='faculty2@test.com', role='faculty')
            faculty2.set_password('pass123')

            staff_it_1 = User(name='Alice IT', email='alice.it@test.com', role='staff', department_id=self.dept_it_id)
            staff_it_1.set_password('pass123')

            staff_it_2 = User(name='Bob IT', email='bob.it@test.com', role='staff', department_id=self.dept_it_id)
            staff_it_2.set_password('pass123')

            staff_fac = User(name='Charlie Fac', email='charlie.fac@test.com', role='staff', department_id=self.dept_fac_id)
            staff_fac.set_password('pass123')

            mgmt = User(name='Mgmt User', email='mgmt@test.com', role='management')
            mgmt.set_password('pass123')

            db.session.add_all([faculty1, faculty2, staff_it_1, staff_it_2, staff_fac, mgmt])
            db.session.commit()

            self.f1_id = faculty1.id
            self.alice_id = staff_it_1.id
            self.bob_id = staff_it_2.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def login(self, email, password='pass123'):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_complete_end_to_end_issue_lifecycle(self):
        # 1. Faculty 1 logs in and submits an Issue
        self.login('faculty1@test.com')
        resp_submit = self.client.post('/faculty/submit', data=dict(
            problem='Projector flickering in Room 101',
            description='Bulb seems to be failing.',
            room_number='Room 101',
            category='IT / Equipment'
        ), follow_redirects=True)

        self.assertEqual(resp_submit.status_code, 200)

        # Verify DB state after submission & automatic routing/assignment
        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Projector flickering in Room 101').first()
            self.assertIsNotNone(issue)
            self.assertEqual(issue.category, 'IT / Equipment')
            self.assertEqual(issue.department.name, 'IT Department')
            self.assertEqual(issue.status, 'Assigned')
            self.assertIsNotNone(issue.assignment)
            # "Alice IT" comes before "Bob IT" alphabetically with equal (0) workload
            self.assertEqual(issue.assignment.staff_id, self.alice_id)
            self.assertIsNone(issue.resolved_at)

            issue_id = issue.id

        # Faculty 1 views dashboard and detail
        resp_fac_dash = self.client.get('/faculty')
        self.assertIn(b'Projector flickering in Room 101', resp_fac_dash.data)
        self.assertIn(b'IT Department', resp_fac_dash.data)
        self.assertIn(b'Assigned', resp_fac_dash.data)

        self.logout()

        # 2. Staff Member Alice IT logs in, acknowledges the issue
        self.login('alice.it@test.com')
        resp_staff_dash = self.client.get('/staff')
        self.assertIn(b'Projector flickering in Room 101', resp_staff_dash.data)

        resp_ack = self.client.post(f'/staff/issue/{issue_id}/action', data=dict(action='acknowledge'), follow_redirects=True)
        self.assertIn(b'Issue acknowledged and marked as In Progress', resp_ack.data)

        with self.app.app_context():
            issue = db.session.get(Issue, issue_id)
            self.assertEqual(issue.status, 'In Progress')
            self.assertIsNone(issue.resolved_at)

        # 3. Staff Member Alice IT resolves the issue
        resp_res = self.client.post(f'/staff/issue/{issue_id}/action', data=dict(action='resolve'), follow_redirects=True)
        self.assertIn(b'Issue resolved successfully', resp_res.data)

        with self.app.app_context():
            issue = db.session.get(Issue, issue_id)
            self.assertEqual(issue.status, 'Resolved')
            self.assertIsNotNone(issue.resolved_at)

        self.logout()

        # 4. Faculty 1 views resolved issue status
        self.login('faculty1@test.com')
        resp_fac_check = self.client.get(f'/faculty/issue/{issue_id}')
        self.assertIn(b'Resolved', resp_fac_check.data)

        self.logout()

        # 5. Management logs in and views the issue
        self.login('mgmt@test.com')
        resp_mgmt_dash = self.client.get('/management')
        self.assertIn(b'Projector flickering in Room 101', resp_mgmt_dash.data)
        self.assertIn(b'IT Department', resp_mgmt_dash.data)
        self.assertIn(b'Alice IT', resp_mgmt_dash.data)
        self.assertIn(b'Resolved', resp_mgmt_dash.data)

        resp_mgmt_det = self.client.get(f'/management/issue/{issue_id}')
        self.assertIn(b'Projector flickering in Room 101', resp_mgmt_det.data)
        self.assertIn(b'Alice IT', resp_mgmt_det.data)

    def test_no_eligible_staff_edge_case_workflow(self):
        # Faculty submits issue under category with no assigned staff (e.g. Academic / Schedule)
        self.login('faculty1@test.com')
        self.client.post('/faculty/submit', data=dict(
            problem='Schedule collision',
            description='Double booked room.',
            room_number='Room 303',
            category='Academic / Schedule'
        ), follow_redirects=True)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Schedule collision').first()
            self.assertEqual(issue.category, 'Academic / Schedule')
            self.assertEqual(issue.department.name, 'Academic Administration')
            self.assertEqual(issue.status, 'Submitted')
            self.assertIsNone(issue.assignment)

        self.logout()

        # Management can see this unassigned issue
        self.login('mgmt@test.com')
        resp_mgmt = self.client.get('/management?status=Submitted')
        self.assertIn(b'Schedule collision', resp_mgmt.data)
        self.assertIn(b'Unassigned', resp_mgmt.data)

    def test_cross_role_and_cross_department_security_restrictions(self):
        # Create an issue assigned to Alice IT
        self.login('faculty1@test.com')
        self.client.post('/faculty/submit', data=dict(
            problem='Alice IT Task',
            room_number='Room 101',
            category='IT / Equipment'
        ))

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Alice IT Task').first()
            issue_id = issue.id

        self.logout()

        # Staff in another department (Charlie Fac) attempts to access / modify Alice's issue -> 404
        self.login('charlie.fac@test.com')
        resp_c_view = self.client.get(f'/staff/issue/{issue_id}')
        self.assertEqual(resp_c_view.status_code, 404)

        resp_c_act = self.client.post(f'/staff/issue/{issue_id}/action', data=dict(action='acknowledge'))
        self.assertEqual(resp_c_act.status_code, 404)

        # Charlie Fac cannot access management
        resp_c_mgmt = self.client.get('/management', follow_redirects=True)
        self.assertIn(b'Unauthorized access', resp_c_mgmt.data)

        self.logout()

        # Faculty 2 attempts to view Faculty 1's issue detail -> 404
        self.login('faculty2@test.com')
        resp_f2_view = self.client.get(f'/faculty/issue/{issue_id}')
        self.assertEqual(resp_f2_view.status_code, 404)

if __name__ == '__main__':
    unittest.main()

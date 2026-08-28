import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Department, Issue, Assignment

class StaffWorkflowTestCase(unittest.TestCase):
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

            # Create Department
            dept = Department(name='IT Department')
            db.session.add(dept)
            db.session.commit()

            # Create Faculty
            faculty = User(name='Faculty User', email='faculty@test.com', role='faculty')
            faculty.set_password('pass123')

            # Create Staff 1 and Staff 2
            s1 = User(name='Staff One', email='staff1@test.com', role='staff', department_id=dept.id)
            s1.set_password('pass123')

            s2 = User(name='Staff Two', email='staff2@test.com', role='staff', department_id=dept.id)
            s2.set_password('pass123')

            # Create Management
            mgmt = User(name='Mgmt User', email='mgmt@test.com', role='management')
            mgmt.set_password('pass123')

            db.session.add_all([faculty, s1, s2, mgmt])
            db.session.commit()

            self.f_id = faculty.id
            self.s1_id = s1.id
            self.s2_id = s2.id
            self.dept_id = dept.id

            # Create Issue assigned to Staff 1
            i1 = Issue(problem='Issue for Staff 1', room_number='101', category='IT / Equipment', status='Assigned', submitted_by=self.f_id, department_id=self.dept_id)
            db.session.add(i1)
            db.session.commit()
            a1 = Assignment(issue_id=i1.id, staff_id=self.s1_id)
            db.session.add(a1)

            # Create Issue assigned to Staff 2
            i2 = Issue(problem='Issue for Staff 2', room_number='202', category='IT / Equipment', status='Assigned', submitted_by=self.s2_id, department_id=self.dept_id)
            db.session.add(i2)
            db.session.commit()
            a2 = Assignment(issue_id=i2.id, staff_id=self.s2_id)
            db.session.add(a2)

            db.session.commit()

            self.i1_id = i1.id
            self.i2_id = i2.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def login(self, email, password='pass123'):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_staff_can_see_own_assigned_issues_and_not_others(self):
        self.login('staff1@test.com')
        response = self.client.get('/staff')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Issue for Staff 1', response.data)
        self.assertNotIn(b'Issue for Staff 2', response.data)

    def test_staff_can_view_own_issue_details_and_not_others(self):
        self.login('staff1@test.com')

        # View own issue -> 200
        resp_own = self.client.get(f'/staff/issue/{self.i1_id}')
        self.assertEqual(resp_own.status_code, 200)
        self.assertIn(b'Issue for Staff 1', resp_own.data)

        # Attempt to view other staff's issue -> 404
        resp_other = self.client.get(f'/staff/issue/{self.i2_id}')
        self.assertEqual(resp_other.status_code, 404)

    def test_assigned_issue_acknowledgement_changes_status_to_in_progress(self):
        self.login('staff1@test.com')
        response = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Issue acknowledged and marked as In Progress', response.data)

        with self.app.app_context():
            issue = db.session.get(Issue, self.i1_id)
            self.assertEqual(issue.status, 'In Progress')
            self.assertIsNone(issue.resolved_at)

    def test_in_progress_issue_resolution_changes_status_and_sets_resolved_at(self):
        self.login('staff1@test.com')
        # Acknowledge first
        self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'))

        # Resolve
        response = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='resolve'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Issue resolved successfully', response.data)

        with self.app.app_context():
            issue = db.session.get(Issue, self.i1_id)
            self.assertEqual(issue.status, 'Resolved')
            self.assertIsNotNone(issue.resolved_at)
            self.assertIsInstance(issue.resolved_at, datetime)

    def test_assigned_issue_cannot_be_directly_resolved(self):
        self.login('staff1@test.com')
        # Directly resolve an 'Assigned' issue without acknowledging
        response = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='resolve'), follow_redirects=True)
        self.assertIn(b"Cannot resolve issue with status &#39;Assigned&#39;.", response.data)

        with self.app.app_context():
            issue = db.session.get(Issue, self.i1_id)
            self.assertEqual(issue.status, 'Assigned')
            self.assertIsNone(issue.resolved_at)

    def test_in_progress_issue_cannot_be_acknowledged_again(self):
        self.login('staff1@test.com')
        self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'))

        # Try acknowledging again
        response = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'), follow_redirects=True)
        self.assertIn(b"Cannot acknowledge issue with status &#39;In Progress&#39;.", response.data)

        with self.app.app_context():
            issue = db.session.get(Issue, self.i1_id)
            self.assertEqual(issue.status, 'In Progress')

    def test_resolved_issue_cannot_be_reopened_or_modified(self):
        self.login('staff1@test.com')
        self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'))
        self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='resolve'))

        # Try acknowledging or resolving resolved issue
        resp_ack = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'), follow_redirects=True)
        self.assertIn(b"Cannot acknowledge issue with status &#39;Resolved&#39;.", resp_ack.data)

        resp_res = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='resolve'), follow_redirects=True)
        self.assertIn(b"Cannot resolve issue with status &#39;Resolved&#39;.", resp_res.data)

    def test_unauthorized_staff_cannot_perform_action_on_other_staff_issue(self):
        self.login('staff2@test.com')
        # Staff 2 attempts action on Staff 1's issue
        response = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'), follow_redirects=True)
        self.assertEqual(response.status_code, 404)

        with self.app.app_context():
            issue = db.session.get(Issue, self.i1_id)
            self.assertEqual(issue.status, 'Assigned')

    def test_faculty_and_management_cannot_perform_staff_actions(self):
        # Faculty attempt
        self.login('faculty@test.com')
        resp_fac = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'), follow_redirects=True)
        self.assertIn(b'Unauthorized access', resp_fac.data)

        # Management attempt
        self.login('mgmt@test.com')
        resp_mgmt = self.client.post(f'/staff/issue/{self.i1_id}/action', data=dict(action='acknowledge'), follow_redirects=True)
        self.assertIn(b'Unauthorized access', resp_mgmt.data)

if __name__ == '__main__':
    unittest.main()

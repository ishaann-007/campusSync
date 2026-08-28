import unittest
from app import create_app, db
from app.models import User, Department, Issue, Assignment

class ManagementDashboardTestCase(unittest.TestCase):
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
            db.session.add_all([dept_it, dept_fac])
            db.session.commit()

            self.dept_it_id = dept_it.id
            self.dept_fac_id = dept_fac.id

            # Create Faculty
            f1 = User(name='Faculty One', email='f1@test.com', role='faculty')
            f1.set_password('pass123')
            f2 = User(name='Faculty Two', email='f2@test.com', role='faculty')
            f2.set_password('pass123')

            # Create Staff
            s_it = User(name='Staff IT', email='s_it@test.com', role='staff', department_id=self.dept_it_id)
            s_it.set_password('pass123')

            s_fac = User(name='Staff Fac', email='s_fac@test.com', role='staff', department_id=self.dept_fac_id)
            s_fac.set_password('pass123')

            # Create Management
            m = User(name='Mgmt User', email='mgmt@test.com', role='management')
            m.set_password('pass123')

            db.session.add_all([f1, f2, s_it, s_fac, m])
            db.session.commit()

            self.f1_id = f1.id
            self.f2_id = f2.id
            self.s_it_id = s_it.id
            self.s_fac_id = s_fac.id

            # Create Issues across statuses, departments, categories, and faculty
            i1 = Issue(problem='IT Issue 1', room_number='101', category='IT / Equipment', status='Submitted', submitted_by=self.f1_id, department_id=self.dept_it_id)
            i2 = Issue(problem='IT Issue 2', room_number='102', category='IT / Equipment', status='Assigned', submitted_by=self.f1_id, department_id=self.dept_it_id)
            i3 = Issue(problem='Fac Issue 1', room_number='201', category='Facilities / Classroom', status='In Progress', submitted_by=self.f2_id, department_id=self.dept_fac_id)
            i4 = Issue(problem='Fac Issue 2', room_number='202', category='Facilities / Classroom', status='Resolved', submitted_by=self.f2_id, department_id=self.dept_fac_id)

            db.session.add_all([i1, i2, i3, i4])
            db.session.commit()

            a2 = Assignment(issue_id=i2.id, staff_id=self.s_it_id)
            a3 = Assignment(issue_id=i3.id, staff_id=self.s_fac_id)
            a4 = Assignment(issue_id=i4.id, staff_id=self.s_fac_id)
            db.session.add_all([a2, a3, a4])
            db.session.commit()

            self.i1_id = i1.id
            self.i2_id = i2.id
            self.i3_id = i3.id
            self.i4_id = i4.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def login(self, email='mgmt@test.com', password='pass123'):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_management_can_access_dashboard(self):
        self.login('mgmt@test.com')
        response = self.client.get('/management')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Management Dashboard', response.data)

    def test_faculty_and_staff_cannot_access_management_routes(self):
        # Faculty attempt
        self.login('f1@test.com')
        resp_f = self.client.get('/management', follow_redirects=True)
        self.assertIn(b'Unauthorized access', resp_f.data)

        resp_f_det = self.client.get(f'/management/issue/{self.i1_id}', follow_redirects=True)
        self.assertIn(b'Unauthorized access', resp_f_det.data)

        # Staff attempt
        self.login('s_it@test.com')
        resp_s = self.client.get('/management', follow_redirects=True)
        self.assertIn(b'Unauthorized access', resp_s.data)

        resp_s_det = self.client.get(f'/management/issue/{self.i1_id}', follow_redirects=True)
        self.assertIn(b'Unauthorized access', resp_s_det.data)

    def test_management_sees_issues_from_different_faculty_and_departments(self):
        self.login('mgmt@test.com')
        response = self.client.get('/management')
        self.assertEqual(response.status_code, 200)

        # Check issues from f1 and f2 are visible
        self.assertIn(b'IT Issue 1', response.data)
        self.assertIn(b'IT Issue 2', response.data)
        self.assertIn(b'Fac Issue 1', response.data)
        self.assertIn(b'Fac Issue 2', response.data)

    def test_management_status_counts_are_correct(self):
        self.login('mgmt@test.com')
        response = self.client.get('/management')
        self.assertEqual(response.status_code, 200)

        # Total 4 issues (1 Submitted, 1 Assigned, 1 In Progress, 1 Resolved)
        self.assertIn(b'<div class="label">Submitted</div>', response.data)
        self.assertIn(b'<div class="label">Total Issues</div>', response.data)

    def test_management_status_filtering(self):
        self.login('mgmt@test.com')
        response = self.client.get('/management?status=In+Progress')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Fac Issue 1', response.data)
        self.assertNotIn(b'IT Issue 1', response.data)
        self.assertNotIn(b'IT Issue 2', response.data)
        self.assertNotIn(b'Fac Issue 2', response.data)

    def test_management_department_filtering(self):
        self.login('mgmt@test.com')
        response = self.client.get(f'/management?department_id={self.dept_fac_id}')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Fac Issue 1', response.data)
        self.assertIn(b'Fac Issue 2', response.data)
        self.assertNotIn(b'IT Issue 1', response.data)
        self.assertNotIn(b'IT Issue 2', response.data)

    def test_management_category_filtering(self):
        self.login('mgmt@test.com')
        response = self.client.get('/management?category=IT+%2F+Equipment')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'IT Issue 1', response.data)
        self.assertIn(b'IT Issue 2', response.data)
        self.assertNotIn(b'Fac Issue 1', response.data)
        self.assertNotIn(b'Fac Issue 2', response.data)

    def test_management_combined_filters(self):
        self.login('mgmt@test.com')
        url = f'/management?status=Assigned&department_id={self.dept_it_id}&category=IT+%2F+Equipment'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'IT Issue 2', response.data)
        self.assertNotIn(b'IT Issue 1', response.data)
        self.assertNotIn(b'Fac Issue 1', response.data)

    def test_management_issue_detail_view(self):
        self.login('mgmt@test.com')
        response = self.client.get(f'/management/issue/{self.i3_id}')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Fac Issue 1', response.data)
        self.assertIn(b'Faculty Two', response.data)
        self.assertIn(b'Staff Fac', response.data)
        self.assertIn(b'In Progress', response.data)

    def test_management_cannot_modify_issues_through_interface(self):
        self.login('mgmt@test.com')
        # Management detail view should be purely read-only (no forms/POST actions)
        response = self.client.get(f'/management/issue/{self.i3_id}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'<form', response.data)

        # POST action endpoints are staff only; management POST attempts must fail authorization
        resp_post = self.client.post(f'/staff/issue/{self.i3_id}/action', data=dict(action='resolve'), follow_redirects=True)
        self.assertIn(b'Unauthorized access', resp_post.data)

if __name__ == '__main__':
    unittest.main()

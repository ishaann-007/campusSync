import unittest
from app import create_app, db
from app.models import User, Department, Issue, Assignment

class StaffAssignmentTestCase(unittest.TestCase):
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

            # Create Faculty
            faculty = User(name='Faculty Member', email='faculty@test.com', role='faculty')
            faculty.set_password('pass123')

            # Create IT Staff (Alice IT & Bob IT)
            staff_alice = User(name='Alice IT', email='alice@test.com', role='staff', department_id=dept_it.id)
            staff_alice.set_password('pass123')

            staff_bob = User(name='Bob IT', email='bob@test.com', role='staff', department_id=dept_it.id)
            staff_bob.set_password('pass123')

            # Create Facilities Staff (Charlie Facilities)
            staff_charlie = User(name='Charlie Facilities', email='charlie@test.com', role='staff', department_id=dept_fac.id)
            staff_charlie.set_password('pass123')

            db.session.add_all([faculty, staff_alice, staff_bob, staff_charlie])
            db.session.commit()

            self.f_id = faculty.id
            self.alice_id = staff_alice.id
            self.bob_id = staff_bob.id
            self.charlie_id = staff_charlie.id
            self.dept_it_id = dept_it.id
            self.dept_fac_id = dept_fac.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def login(self, email='faculty@test.com', password='pass123'):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_only_staff_from_responsible_department_are_eligible(self):
        self.login()
        # Submit Facilities issue -> should assign to Charlie Facilities, NOT Alice/Bob IT
        self.client.post('/faculty/submit', data=dict(
            problem='Broken desk',
            description='Desk leg broken',
            room_number='Room 101',
            category='Facilities / Classroom'
        ), follow_redirects=True)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Broken desk').first()
            self.assertEqual(issue.status, 'Assigned')
            self.assertIsNotNone(issue.assignment)
            self.assertEqual(issue.assignment.staff_id, self.charlie_id)

    def test_equal_workloads_resolved_alphabetically(self):
        self.login()
        # Initial submission for IT Department where Alice IT and Bob IT both have 0 workload.
        # "Alice IT" comes before "Bob IT" alphabetically.
        self.client.post('/faculty/submit', data=dict(
            problem='Network down',
            description='No internet',
            room_number='Room 202',
            category='IT / Equipment'
        ), follow_redirects=True)

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Network down').first()
            self.assertEqual(issue.status, 'Assigned')
            self.assertEqual(issue.assignment.staff_id, self.alice_id)

    def test_staff_with_fewer_active_issues_selected(self):
        self.login()
        # Issue 1: Assigned to Alice IT (Alice now has 1 active issue, Bob has 0)
        self.client.post('/faculty/submit', data=dict(
            problem='IT Issue 1',
            description='Issue 1',
            room_number='101',
            category='IT / Equipment'
        ))

        # Issue 2: Submitted. Since Bob has 0 active issues and Alice has 1, Bob IT should be selected.
        self.client.post('/faculty/submit', data=dict(
            problem='IT Issue 2',
            description='Issue 2',
            room_number='102',
            category='IT / Equipment'
        ))

        with self.app.app_context():
            issue1 = Issue.query.filter_by(problem='IT Issue 1').first()
            issue2 = Issue.query.filter_by(problem='IT Issue 2').first()

            self.assertEqual(issue1.assignment.staff_id, self.alice_id)
            self.assertEqual(issue2.assignment.staff_id, self.bob_id)

    def test_assigned_and_in_progress_count_toward_active_workload(self):
        with self.app.app_context():
            # Create pre-existing Assigned issue for Alice IT
            i1 = Issue(problem='Pre1', room_number='1', category='IT / Equipment', status='Assigned', submitted_by=self.f_id, department_id=self.dept_it_id)
            db.session.add(i1)
            db.session.commit()
            a1 = Assignment(issue_id=i1.id, staff_id=self.alice_id)
            db.session.add(a1)

            # Create pre-existing In Progress issue for Alice IT
            i2 = Issue(problem='Pre2', room_number='2', category='IT / Equipment', status='In Progress', submitted_by=self.f_id, department_id=self.dept_it_id)
            db.session.add(i2)
            db.session.commit()
            a2 = Assignment(issue_id=i2.id, staff_id=self.alice_id)
            db.session.add(a2)

            db.session.commit()

        self.login()
        # Next issue should go to Bob IT (0 active issues vs Alice's 2 active issues)
        self.client.post('/faculty/submit', data=dict(
            problem='New IT Issue',
            room_number='103',
            category='IT / Equipment'
        ))

        with self.app.app_context():
            new_issue = Issue.query.filter_by(problem='New IT Issue').first()
            self.assertEqual(new_issue.assignment.staff_id, self.bob_id)

    def test_resolved_issues_do_not_count_toward_active_workload(self):
        with self.app.app_context():
            # Alice IT has 2 Resolved issues
            for idx in range(2):
                iss = Issue(problem=f'Resolved {idx}', room_number='10', category='IT / Equipment', status='Resolved', submitted_by=self.f_id, department_id=self.dept_it_id)
                db.session.add(iss)
                db.session.commit()
                asg = Assignment(issue_id=iss.id, staff_id=self.alice_id)
                db.session.add(asg)

            # Bob IT has 1 Assigned issue
            b_iss = Issue(problem='Bob Active', room_number='11', category='IT / Equipment', status='Assigned', submitted_by=self.f_id, department_id=self.dept_it_id)
            db.session.add(b_iss)
            db.session.commit()
            b_asg = Assignment(issue_id=b_iss.id, staff_id=self.bob_id)
            db.session.add(b_asg)

            db.session.commit()

        self.login()
        # Alice active workload = 0, Bob active workload = 1.
        # New issue must go to Alice IT.
        self.client.post('/faculty/submit', data=dict(
            problem='Test Resolved Workload',
            room_number='105',
            category='IT / Equipment'
        ))

        with self.app.app_context():
            new_issue = Issue.query.filter_by(problem='Test Resolved Workload').first()
            self.assertEqual(new_issue.assignment.staff_id, self.alice_id)

    def test_no_eligible_staff_leaves_issue_submitted(self):
        self.login()
        # Submit Academic / Schedule issue where no department / staff exists in test DB setup
        self.client.post('/faculty/submit', data=dict(
            problem='Classroom collision',
            room_number='303',
            category='Academic / Schedule'
        ))

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Classroom collision').first()
            self.assertEqual(issue.status, 'Submitted')
            self.assertIsNone(issue.assignment)

    def test_faculty_cannot_manually_choose_or_override_staff_assignment(self):
        self.login()
        # Attempt to pass staff_id directly in form submit
        self.client.post('/faculty/submit', data=dict(
            problem='Override Staff Test',
            room_number='101',
            category='IT / Equipment',
            staff_id=self.bob_id
        ))

        with self.app.app_context():
            issue = Issue.query.filter_by(problem='Override Staff Test').first()
            # Alice IT is first alphabetically with 0 active workload, so algorithm assigns Alice IT regardless of staff_id in form
            self.assertEqual(issue.assignment.staff_id, self.alice_id)

if __name__ == '__main__':
    unittest.main()

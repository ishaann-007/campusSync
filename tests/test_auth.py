import unittest
from app import create_app, db
from app.models import User, Department

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SECRET_KEY': 'test_secret'
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            
            # Setup test department and users
            dept = Department(name='IT Department')
            db.session.add(dept)
            db.session.commit()

            f_user = User(name='Faculty User', email='faculty@test.com', role='faculty')
            f_user.set_password('facpass')
            
            s_user = User(name='Staff User', email='staff@test.com', role='staff', department_id=dept.id)
            s_user.set_password('staffpass')

            m_user = User(name='Management User', email='management@test.com', role='management')
            m_user.set_password('mgmtpass')

            db.session.add_all([f_user, s_user, m_user])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_password_hashing(self):
        with self.app.app_context():
            user = User.query.filter_by(email='faculty@test.com').first()
            self.assertNotEqual(user.password_hash, 'facpass')
            self.assertTrue(user.check_password('facpass'))
            self.assertFalse(user.check_password('wrongpass'))

    def test_valid_login_and_logout(self):
        # Faculty login
        response = self.login('faculty@test.com', 'facpass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Faculty Dashboard', response.data)

        # Logout
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)

    def test_invalid_login(self):
        response = self.login('faculty@test.com', 'wrongpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password', response.data)

    def test_unauthenticated_access_protection(self):
        response = self.client.get('/faculty', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

        response = self.client.get('/staff', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

        response = self.client.get('/management', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_role_based_access_control(self):
        # Log in as Faculty
        self.login('faculty@test.com', 'facpass')

        # Attempt to access Staff route
        response = self.client.get('/staff', follow_redirects=True)
        self.assertIn(b'Unauthorized access', response.data)
        self.assertIn(b'Faculty Dashboard', response.data)

        # Attempt to access Management route
        response = self.client.get('/management', follow_redirects=True)
        self.assertIn(b'Unauthorized access', response.data)

if __name__ == '__main__':
    unittest.main()

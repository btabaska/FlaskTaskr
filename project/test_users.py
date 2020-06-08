
import os
import unittest

from views import app,db
from _config import basedir
from models import User
from testing_helper import login, register, logout, create_user, create_task

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        register(self, 'Michael', 'michael@realpython.com', 'python', 'python')

    #executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #each test should start with test
    def test_user_setup(self):
        new_user = User('Bob', 'Bob@mherman.org', 'michealherman')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == 'Bob'

    def test_users_login(self):
        response = login(self, 'foo', 'bar')
        self.assertIn(b'Invalid username or password', response.data)
        response = login(self, 'Michael', 'python')
        self.assertIn(b'Welcome!', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = register(self, 'brandon', 'brandon@realpython.com', 'python', 'python')
        self.assertIn(b'Thanks for registering, please login.', response.data)
        self.app.get('register/', follow_redirects=True)
        response = register(self,
            'Michael', 'michael@realpython.com', 'python', 'python'
        )
        self.app.get('register/', follow_redirects=True)
        response = register(self,
            'Michael', 'michael@realpython.com', 'python', 'python'
        )
        self.assertIn(
            b'That username and/or email already exists.',
            response.data
        )

    def test_logged_in_users_can_logout(self):
        login(self, 'Michael', 'python')
        response = logout(self)
        self.assertIn(b'Goodbye!', response.data)

    def test_default_user_role(self):

        db.session.add(
            User(
                'Johnny',
                'john@doe.com',
                'johnny'
            )
        )

        db.session.commit()
        users = db.session.query(User).all()
        print(users)
        for user in users:
            self.assertEquals(user.role, 'user')



if __name__ == '__main__':
    unittest.main()

import os
import unittest

from project import app,db
from project._config import basedir
from project.models import User
from tests.testing_helper import login, register, logout, create_task,create_admin_user

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

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
        self.assertIn(b'Thanks for registering. Please login.', response.data)
        self.app.get('register/', follow_redirects=True)
        response = register(self,
            'Michael', 'michael@realpython.com', 'python', 'python'
        )
        self.app.get('register/', follow_redirects=True)
        response = register(self,
            'Michael', 'michael@realpython.com', 'python', 'python'
        )
        self.assertIn(
            b'That username and/or email already exist.',
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

    def test_task_template_displays_logged_in_user_name(self):
        login(self, 'Michael', 'python')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'Michael', response.data)

    def test_users_cannot_see_task_modify_links_for_tasks_not_created_by_them(self):
        login(self, 'Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        create_task(self)
        logout(self)
        register(self, 'Fletcher', 'fletcher@realpython.com', 'python101', 'python101')
        response = login(self, 'Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        self.assertNotIn(b'Mark as complete', response.data)
        self.assertNotIn(b'Delete', response.data)

    def test_users_can_see_task_modify_links_for_tasks_created_by_them(self):
        login(self, 'Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        create_task(self)
        logout(self)
        register(self, 'Fletcher', 'fletcher@realpython.com', 'python101', 'python101')
        login(self, 'Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = create_task(self)
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'complete/2/', response.data)

    def test_admin_users_can_see_task_modify_links_for_all_tasks(self):
        login(self, 'Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        create_task(self)
        logout(self)
        create_admin_user(self)
        login(self, 'AdminUser', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)
        response = create_task(self)
        self.assertIn(b'complete/1/', response.data)
        self.assertIn(b'delete/1/', response.data)
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)







if __name__ == '__main__':
    unittest.main()
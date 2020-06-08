
import os
import unittest

from views import app,db
from _config import basedir
from models import User
from testing_helper import create_task, create_user, logout, login, register, create_admin_user

TEST_DB = 'test.db'

class TestTasks(unittest.TestCase):
    print('Hello World')

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        register(self, 'Micheal', 'michael@realpython.com', 'python', 'python')
        login(self, 'Micheal', 'python')

    #executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_form_is_present(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your task list', response.data)

    def test_invalid_form_data(self):
        logout(self)
        response = login(self, 'alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.', response.data)

    def test_logged_in_users_can_access_tasks_page(self):
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)
        logout(self)
        response2 = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response2.data)

    def test_users_can_add_tasks(self):
        self.app.get('tasks/', follow_redirects=True)
        response = create_task(self)
        self.assertIn(
            b'New entry was successfully posted. Thanks', response.data
        )
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='',
            priority='1',
            posted_date='02/05/2014',
            status='1'
        ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.app.get('tasks/', follow_redirects=True)
        create_task(self)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertIn(b'The task is complete. Nice', response.data)

    def test_users_can_delete_tasks(self):
        self.app.get('tasks/', follow_redirects=True)
        create_task(self)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.app.get('tasks/', follow_redirects=True)
        create_task(self)
        logout(self)
        create_user(self, 'Fletcher', 'fletcher@realpython.com', 'python101')
        login(self, 'Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'The task is complete. Nice', response.data)
        self.assertIn(b'You can only update tasks that belong to you.', response.data)

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.app.get('tasks', follow_redirects=True)
        create_task(self)
        logout(self)
        create_user(self, 'Fletcher', 'fletcher@realpython.com', 'python101')
        login(self, 'Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'You can only delete tasks that belong to you.', response.data)

    def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
        self.app.get('tasks/', follow_redirects=True)
        create_task(self)
        logout(self)
        create_admin_user(self)
        login(self, 'AdminUser', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(b'You can only update tasks that belong to you.', response.data)

    def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.app.get('tasks/', follow_redirects=True)
        create_task(self)
        logout(self)
        create_admin_user(self)
        login(self, 'AdminUser', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertNotIn(b'You can only delete tasks that belong to you.', response.data)










if __name__ == '__main__':
    unittest.main()
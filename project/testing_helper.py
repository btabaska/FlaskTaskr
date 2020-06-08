
import os
import unittest

from views import app,db
from _config import basedir
from models import User

TEST_DB = 'test.db'

def login(self, name, password):
    return self.app.post('/', data=dict(name=name, password=password), follow_redirects = True)

#helper function to register users
def register(self, name, email, password, confirm):
    return self.app.post(
        'register/',
          data=dict(name=name, email=email, password=password, confirm=confirm), follow_redirects = True
     )

 #helper function to logout
def logout(self):
     return self.app.get('logout/', follow_redirects=True)

#helper function to create user
def create_user(self, name, email, password):
     new_user = User(name=name, email=email, password=password)
     db.session.add(new_user)
     db.session.commit()


def create_task(self):
    return self.app.post('add/', data=dict(
         name='Go to the bank',
         due_date='10/08/2016',
         priority='1',
          posted_date='10/08/2016',
         status='1'
     ), follow_redirects=True)

def create_admin_user(self):
    new_user = User(name='AdminUser', email='Admin@realpython.com', password='allpowerful', role='admin')
    db.session.add(new_user)
    db.session.commit()
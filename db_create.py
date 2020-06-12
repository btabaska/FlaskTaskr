# project/db_create.py

from project import db
from datetime import date
from project.models import Task, User

#create the database and the db table
db.create_all()

db.session.commit()
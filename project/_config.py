import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktasllkr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'myprecious'
DEBUG = True

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

#The database URL
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH


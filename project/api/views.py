# project/api/views.py


from functools import wraps
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response, request, render_template
import datetime
from flask_restful import Resource, Api, reqparse

from project import db, bcrypt
from project.models import Task
from project.models import User

from flask_httpauth import HTTPBasicAuth

################
#### config ####
################

api_blueprint = Blueprint('api', __name__)

#working with flask_restful
api = Api(api_blueprint)

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('name')
parser.add_argument('due_date')
parser.add_argument('priority')

auth = HTTPBasicAuth()
##########################
#### helper functions ####
##########################

def open_tasks():
    return db.session.query(Task).filter_by(
        status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(
        status='0').order_by(Task.due_date.asc())

@auth.verify_password
def verify_password(username, password):
    user = db.session.query(User).filter_by(name = username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return True
    return False

###################################
#### Working with flask_restful####
###################################

class ReadTask(Resource):
    def get(self, id):
        result = db.session.query(Task).filter_by(task_id=id).first()
        if result:
            json_result = {
                'task_id': result.task_id,
                'task name': result.name,
                'due date': str(result.due_date),
                'priority': result.priority,
                'posted date': str(result.posted_date),
                'status': result.status,
                'user id': result.user_id

            }
            return jsonify(items=json_result)
        else:
            result = {'error': 'Element does not exist'}
            code = 404
            return make_response(jsonify(result), code)
api.add_resource(ReadTask, '/api/v1/tasks/<int:id>')

class ReadTasks(Resource):
    def get(self):
        results = db.session.query(Task).limit(10).offset(0).all()
        json_results = []
        for result in results:
            data = {
                'task_id': result.task_id,
                'task name': result.name,
                'due date': str(result.due_date),
                'priority': result.priority,
                'posted date': str(result.posted_date),
                'status': result.status,
                'user id': result.user_id
            }
            json_results.append(data)
        return jsonify(items=json_results)
api.add_resource(ReadTasks, '/api/v1/tasks/')

class CreateTask(Resource):
    @auth.login_required()
    def post(self):
        args=parser.parse_args()
        result = db.session.query(User).filter_by(name=args['username']).first()
        if result:
            new_task = Task(
                args['name'],
                datetime.datetime.strptime(args['due_date'], '%m/%d/%Y'),
                args['priority'],
                datetime.datetime.utcnow(),
                '1',
                result.id
            )
            db.session.add(new_task)
            db.session.commit()
            json_results = {
                'task_name' : new_task.name,
                'due_date' :  new_task.due_date,
                'priority' : new_task.priority,
                'posted date' : new_task.posted_date,
                'status' : new_task.status,
                'user id' : new_task.user_id
            }
            return jsonify(json_results)
        else:
            result = {'error': 'User does not exist'}
            code = 404
            return make_response(jsonify(result), code)
api.add_resource(CreateTask, '/api/create/')


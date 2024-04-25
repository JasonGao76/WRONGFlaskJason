import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.classes import Classes

classes_api = Blueprint('classes_api', __name__,
                   url_prefix='/api/classes')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(classes_api)

# this code was written by a collaborator
class ClassesAPI:
    class _CRUD(Resource):  # define GET request
        def get(self): # read Method
            CharClasses = Classes.query.all()    # read/extract all users from database
            json_ready = [CharClass.read() for CharClass in CharClasses]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
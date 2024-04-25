import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.CurrentChars import CurrentChar

import numpy as np

currentchar_api = Blueprint('currentchar_api', __name__,
                   url_prefix='/api/currentchar')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(currentchar_api)

# most of this (except for the data validation and processing of range / movement, which was mine) was done by a collaborator
class CurrentCharAPI:        
    class _CRUD(Resource):  # define POST, GET, and PUT requests
        def post(self): # POST (create) 
            # read data
            body = request.get_json()

            # validate data
            classname = body.get('classname')
            if classname is None or len(classname) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400

            health = body.get('health')
            if health is None:
                return {'message': f'Health is missing'}, 400

            attack = body.get('attack')
            if attack is None:
                return {'message': f'Attack is missing'}, 400

            range = body.get('range')
            if range is None:
                return {'message': f'Range is missing'}, 400

            movement = body.get('movement')
            if movement is None:
                return {'message': f'Movement is missing'}, 400

            # setup USER OBJECT
            co = CurrentChar(
                classname = classname,
                health = health,
                attack = attack,
                range = str(range).lower()=="true",
                movement = str(movement).lower()=="true"
            )
        
            # create user in database
            CharClass = co.create()

            # success returns json of user
            if CharClass:
                return jsonify(CharClass.read())

        def get(self): # GET (read)
            CurrentCharacter = CurrentChar.query.all() # read/extract all users from database
            json_ready = [CurrentCharacter.read() for CurrentCharacter in CurrentCharacter]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object

        def put(self): # PUT (update)
            # get preset class data
            body = request.get_json() # get the body of the request
            classname = body.get('classname') # get the classname
            health = body.get('health') # get the health
            attack = body.get('attack') # get the attack
            range = body.get('range') # get range boolean
            movement = body.get('movement') # get movement boolean
            CurrentCharacter = CurrentChar.query.all() # get users

            # turn range and movement from boolean string to number (1 is true, 0 is false)
            if range == "true" or range == 1: # both added as the initial character creation uses true/false, but updates use 1/0
                range = 1
            else:
                range = 0
            
            if movement == "true" or movement == 1:
                movement = 1
            else:
                movement = 0
            
            # create current character using preset class data
            CurrentCharacter[0].update(classname, health, attack, range, movement)
            return f"{CurrentCharacter[0].read()} Updated"
    
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
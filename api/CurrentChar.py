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

class CurrentCharAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        # @token_required
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            classname = body.get('classname')
            if classname is None or len(classname) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            health = body.get('health')
            # if health is None or len(health) < 2:
            #     return {'message': f'Name is missing, or is less than 2 characters'}, 400
            attack = body.get('attack')
            # if attack is None or len(attack) < 2:
            #     return {'message': f'Name is missing, or is less than 2 characters'}, 400
            range = body.get('range')
            # if range is None or len(range) < 2:
            #     return {'message': f'Name is missing, or is less than 2 characters'}, 400
            movement = body.get('movement')
            # if movement is None or len(movement) < 2:
            #     return {'message': f'Name is missing, or is less than 2 characters'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            co = CurrentChar(classname=classname,
                             health=health,
                             attack=attack,
                             range=str(range).lower()=="true",
                             movement=str(movement).lower()=="true")
        
            ''' #2: Key Code block to add user to database '''
            # create user in database
            CharClass = co.create()
            # success returns json of user
            if CharClass:
                return jsonify(CharClass.read())

        # @token_required
        def get(self): # Read Method
            CurrentCharacter = CurrentChar.query.all()    # read/extract all users from database
            json_ready = [CurrentCharacter.read() for CurrentCharacter in CurrentCharacter]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

        def put(self):
            body = request.get_json() # get the body of the request
            classname = body.get('classname')
            health = body.get('health') # get the UID (Know what to reference)
            attack = body.get('attack') # get name (to change)
            range = body.get('range') # get name (to change)
            movement = body.get('movement') # get name (to change)
            CurrentCharacter = CurrentChar.query.all() # get users
            # for CurrentCharacter in CurrentCharacter:
                # if CurrentCharacter.classname == classname: # find user with matching uid
            # check length of current character todo
            CurrentCharacter[0].update(classname,health,attack,range==True,movement==True) # update info
            return f"{CurrentCharacter[0].read()} Updated"
    
    # class _ML(Resource):
    #     def probability():
    #         try:
    #             body = request.get_json()
    #             if not body: return {
    #                 "message": "Please provide user details",
    #                 "data": None,
    #                 "error": "Bad request"
    #             }, 400
    #         except Exception as e:
    #             return {
    #                 "message": "Something went wrong!",
    #                 "error": str(e),
    #                 "data": None
    #             }, 500
                        
    #         # Machine Learning Titanic model to predict probability of living
    #         # Define a new passenger
    #         passenger = pd.DataFrame({ ## see above for what each one is
    #             'name': ['Jason Gao'],
    #             'pclass': [1], 
    #             'sex': ['male'],
    #             'age': [18],
    #             'sibsp': [1],
    #             'parch': [2],
    #             'fare': [36.00], # median fare (16) picked assuming it is 2nd class
    #             'embarked': ['S'], # majority of passengers embarked in Southampton
    #             'alone': [False] # travelling with family
    #         })

    #         display(passenger)
    #         new_passenger = passenger.copy()

    #         # Preprocess the new passenger data
    #         new_passenger['sex'] = new_passenger['sex'].apply(lambda x: 1 if x == 'male' else 0)
    #         new_passenger['alone'] = new_passenger['alone'].apply(lambda x: 1 if x == True else 0)

    #         # Encode 'embarked' variable
    #         onehot = enc.transform(new_passenger[['embarked']]).toarray()
    #         cols = ['embarked_' + val for val in enc.categories_[0]]
    #         new_passenger[cols] = pd.DataFrame(onehot, index=new_passenger.index)
    #         new_passenger.drop(['name'], axis=1, inplace=True)
    #         new_passenger.drop(['embarked'], axis=1, inplace=True)

    #         # Predict the survival probability for the new passenger
    #         _, alive_proba = np.squeeze(logreg.predict_proba(new_passenger))

    #         # Print the survival probability
    #         print('Survival probability: {:.2%}'.format(alive_proba))

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    # api.add_resource(_ML, '/machinelearning')
    
    # class _Security(Resource):
    #     def post(self):
    #         try:
    #             body = request.get_json()
    #             if not body:
    #                 return {
    #                     "message": "Please provide user details",
    #                     "data": None,
    #                     "error": "Bad request"
    #                 }, 400
    #             ''' Get Data '''
    #             uid = body.get('uid')
    #             if uid is None:
    #                 return {'message': f'User ID is missing'}, 400
    #             password = body.get('password')
                
    #             ''' Find user '''
    #             user = User.query.filter_by(_uid=uid).first()
    #             if user is None or not user.is_password(password):
    #                 return {'message': f"Invalid user id or password"}, 400
    #             if user:
    #                 try:
    #                     token = jwt.encode(
    #                         {"_uid": user._uid},
    #                         current_app.config["SECRET_KEY"],
    #                         algorithm="HS256"
    #                     )
    #                     resp = Response("Authentication for %s successful" % (user._uid))
    #                     resp.set_cookie("jwt", token,
    #                             max_age=3600,
    #                             secure=True,
    #                             httponly=True,
    #                             path='/',
    #                             samesite='None'  # This is the key part for cross-site requests

    #                             # domain="frontend.com"
    #                             )
    #                     return resp
    #                 except Exception as e:
    #                     return {
    #                         "error": "Something went wrong",
    #                         "message": str(e)
    #                     }, 500
    #             return {
    #                 "message": "Error fetching auth token!",
    #                 "data": None,
    #                 "error": "Unauthorized"
    #             }, 404
    #         except Exception as e:
    #             return {
    #                     "message": "Something went wrong!",
    #                     "error": str(e),
    #                     "data": None
    #             }, 500

            

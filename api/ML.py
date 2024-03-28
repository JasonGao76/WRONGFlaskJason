from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.ML import ML
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

ml_bp = Blueprint("ml", __name__, url_prefix = '/api/ml')
ml_api = Api(ml_bp)

class MLAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("socialclass", required=True, type=int)
        parser.add_argument("age", required=True, type=int)
        parser.add_argument("sex", required=True, type=str)
        parser.add_argument("siblings", required=True, type=int)
        parser.add_argument("family", required=True, type=int)
        parser.add_argument("fare", required=True, type=int)
        parser.add_argument("port", required=True, type=str)
        parser.add_argument("alone", required=True, type=str)
        args = parser.parse_args()
        
        titanic_data = sns.load_dataset('titanic')
        
        passenger = pd.DataFrame({
            'pclass': [args["socialclass"]],
            'sex': [args["sex"]],
            'age': [args["age"]],
            'sibsp': [args["siblings"]],
            'parch': [args["family"]],
            'fare': [args["fare"]],
            'embarked': [args["port"]],
            'alone': [args["alone"]]
        })
        
        td = titanic_data
        td.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
        td.dropna(inplace=True) # drop rows with at least one missing value, after dropping unuseful columns
        td['sex'] = td['sex'].apply(lambda x: 1 if x == 'm' else 0)
        td['alone'] = td['alone'].apply(lambda x: 1 if x == 'y' else 0)

        # Encode categorical variables
        enc = OneHotEncoder(handle_unknown='ignore')
        enc.fit(td[['embarked']])
        onehot = enc.transform(td[['embarked']]).toarray()
        cols = ['embarked_' + val for val in enc.categories_[0]]
        td[cols] = pd.DataFrame(onehot)
        td.drop(['embarked'], axis=1, inplace=True)
        td.dropna(inplace=True) # drop rows with at least one missing value, after preparing the data
        
        X = td.drop('survived', axis=1) # all except 'survived'
        y = td['survived'] # only 'survived'

        # Split arrays in random train 70%, random test 30%, using stratified sampling (same proportion of survived in both sets) and a fixed random state (42
        # The number 42 is often used in examples and tutorials because of its cultural significance in fields like science fiction (it's the "Answer to the Ultimate Question of Life, The Universe, and Everything" in The Hitchhiker's Guide to the Galaxy by Douglas Adams). But in practice, the actual value doesn't matter; what's important is that it's set to a consistent value.
        # X_train is the DataFrame containing the features for the training set.
        # X_test is the DataFrame containing the features for the test set.
        # y-train is the 'survived' status for each passenger in the training set, corresponding to the X_train data.
        # y_test is the 'survived' status for each passenger in the test set, corresponding to the X_test data.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Train a decision tree classifier
        dt = DecisionTreeClassifier()
        dt.fit(X_train, y_train)

        # Test the model
        y_pred = dt.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print('DecisionTreeClassifier Accuracy: {:.2%}'.format(accuracy))  

        # Train a logistic regression model
        logreg = LogisticRegression()
        logreg.fit(X_train, y_train)

        # Test the model
        y_pred = logreg.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        new_passenger = passenger.copy()

        # Preprocess the new passenger data
        new_passenger['sex'] = new_passenger['sex'].apply(lambda x: 1 if x == 'm' else 0)
        new_passenger['alone'] = new_passenger['alone'].apply(lambda x: 1 if x == 'y' else 0)

        # Encode 'embarked' variable
        onehot = enc.transform(new_passenger[['embarked']]).toarray()
        cols = ['embarked_' + val for val in enc.categories_[0]]
        new_passenger[cols] = pd.DataFrame(onehot, index=new_passenger.index)
        new_passenger.drop(['embarked'], axis=1, inplace=True)
        
        dead_proba, alive_proba = np.squeeze(logreg.predict_proba(new_passenger))
        
        ml = ML(args["socialclass"],args["age"],args["sex"],args["siblings"],args["family"], args["fare"], args["port"], args["alone"], alive_proba)

        try:
            db.session.add(ml)
            db.session.commit()
            return alive_proba
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

ml_api.add_resource(MLAPI, "/")
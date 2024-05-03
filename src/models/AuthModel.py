from flask import jsonify
from flask_jwt_extended import create_access_token
from models.entities.User import UserSession
from database.db import session

class AuthModel:
        
    @classmethod
    def login(cls, username, password):
        try:
            query = session.query(UserSession)
            user_from_db = query.filter(UserSession.username == username).first()
            print(user_from_db.password)
            print(password)
            if user_from_db.username == username and user_from_db.password.strip() == password:
                access_token = create_access_token(identity=user_from_db.id)
                user_json = user_from_db.to_JSON_session()
                return jsonify({'token': access_token, 'user': user_json})
            else:
                print("Estoy en else")
                return jsonify({'message': 'Invalid username or password'}), 401
        except Exception as ex:

            print("Estoy en login Model")
            raise Exception(ex)

    @classmethod
    def user_role(cls, user):
        try:
            query = session.query(UserSession)
            user_from_db = query.filter_by(username=user.username).first()
            if user_from_db:
                return jsonify({'role': user_from_db.rol})
            else:
                return None, 400
        except Exception as ex:
            raise Exception(ex)

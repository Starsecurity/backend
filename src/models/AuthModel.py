from flask import jsonify
from flask_jwt_extended import create_access_token
from models.entities.User import User
from database.db import session

class AuthModel:
        
    @classmethod
    def login(cls, username, password):
        try:
            query = session.query(User)
            user_from_db = query.filter_by(username=username).first()
            if user_from_db and user_from_db.check_password(password):
                access_token = create_access_token(identity=user_from_db.id)
                user_json = user_from_db.to_JSON()
                return jsonify({'token': access_token, 'user': user_json})
            else:
                return jsonify({'message': 'Invalid username or password'}), 401
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def user_role(cls, user):
        try:
            query = session.query(user)
            user_from_db = query.filter_by(username=user.username).first()
            if user_from_db:
                return jsonify({'role': user_from_db.rol})
            else:
                return None, 400
        except Exception as ex:
            raise Exception(ex)

# Auth.py
from flask import Blueprint, jsonify, request
from models.AuthModel import AuthModel
from models.entities.User import User
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager

main = Blueprint("auth_blueprint", __name__)

@main.route('/login', methods=['POST'])
def login():
    try:
        user = User(id,request.json['username'],request.json['password'])
        user_data = AuthModel.login(user)
        return user_data
    except Exception as ex:
        return  jsonify({'message': str(ex)}), 500
    
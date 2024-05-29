#
from flask import Blueprint, jsonify, request
from models.AuthModel import AuthModel
from models.entities.User import UserSession, Users
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from database.db import session

main = Blueprint("auth_blueprint", __name__)


@main.route('/login', methods=['POST'])
def login():
    try:
        # Obtener datos del usuario desde la solicitud JSON
        username = request.json.get('name')
        password = request.json.get('password')
        # Verificar que se hayan proporcionado tanto el nombre de usuario como la contraseña
        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400
            

        # Llamar a la función login de AuthModel pasando el username y password
        user_data = AuthModel.login(username, password)

        # Devolver los datos del usuario
        return user_data
    except Exception as ex:
        session.rollback()
        return jsonify({'message': str(ex)}), 500


@main.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

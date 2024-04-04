from flask import Blueprint, jsonify, request
import uuid

from models.entities.User import User
from models.UserModel import UserModel

main = Blueprint("register_blueprint", __name__)

@main.route('/', methods=['POST'])

def add_user():
    
    try:
        username = request.json['username']
        password = request.json['password']
        nombre_completo = request.json['nombre_completo']
        cedula = request.json['cedula']
        telefono = int(request.json['telefono'])
        id = uuid.uuid4()
        user = User(str(id),username, password, nombre_completo,cedula,telefono)
        
        affected_rows = UserModel.add_user(user)

        if affected_rows == 1:
            return jsonify(user.cedula)
        else:
            return jsonify({'message': "Error on insert"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
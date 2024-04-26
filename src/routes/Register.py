#Register.py
from flask import Blueprint, jsonify, request

import uuid

from models.entities.User import User
from models.UserModel import UserModel

main = Blueprint("register_blueprint", __name__)

@main.route('', methods=['POST'])
def add_user():
    
    try:
        # Obtener datos del formulario
        username = request.json['name']
        password = request.json['password']
        nombre_completo = request.json['nombre_completo']
        cedula = request.json['cedula']
        telefono = int(request.json['telefono'])
        huella = request.json.get('fingerprint')
        foto_perfil = request.json.get('profilePhoto')
        default_role = "usuario"
        delante_cedula = request.json.get('delante_cedula')
        reverso_cedula = request.json.get('reverso_cedula')
        
        id = uuid.uuid4()
        user = User(str(id), username, password, nombre_completo, cedula, telefono,foto_perfil,huella,default_role,delante_cedula,reverso_cedula)
        
        affected_rows = UserModel.add_user(user)
        
        if affected_rows == 1:
            return user.to_JSON()
        else:
            return jsonify({'message': "Error on insert"}), 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

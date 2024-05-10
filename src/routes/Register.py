#Register.py
from flask import Blueprint, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

import uuid

from models.entities.User import Users,UserSession
from models.UserModel import UserModel

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

main = Blueprint("register_blueprint", __name__)

@main.route('addsession', methods=['POST'])
def add_user_session():
    try:
        # Generar un ID único para el usuario
        id = uuid.uuid4()

        # Obtener datos del formulario
        username = request.json['name']
        password = request.json['password']
        correo=request.json['correo']
        default_role = "usuario"
        # Crear la instancia de User con el ID generado
        username_prueba = UserModel.get_user_username(username)
        if username_prueba is not None:
            return jsonify({'message':'El username ya existe ya existe'}),409
        #user.id = str(id)
        #hashed_password = generate_password_hash(password)
        user = UserSession(str(id), username, password, correo,default_role)
        # Agregar el usuario a la base de datos
        affected_rows = UserModel.add_user_session(user)
        print(affected_rows)
            

        if affected_rows != 1:
            return user.to_JSON_session()
        else:
                
            return jsonify({'message': "Error on insert"}), 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

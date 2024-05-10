#Register.py
from flask import Blueprint, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

import uuid

from models.entities.User import Users,UserSession
from models.UserModel import UserModel


main = Blueprint("register_blueprint", __name__)

<<<<<<< HEAD
@main.route('addsession', methods=['POST'])
=======
@main.route('adduser/<id>', methods=['POST'])
def add_user(id):
    try:
        # Generar un ID único para el usuario
        id_user = uuid.uuid4()

        # Obtener datos del formulario
        nombre_completo = request.json['nombre_completo']
        cedula = request.json['cedula']
        telefono = request.json['telefono']
        huella = request.json['fingerprint']
        foto_perfil = request.json['profilePhoto']
        delante_cedula =request.json['delante_cedula']
        reverso_cedula = request.json['reverso_cedula']
        user_session=UserModel.get_user_by_id_Session(id)
        
        if user_session:
            user_session_id = user_session.get('id')
        else:
            return jsonify({'message': 'No se pudo encontrar el usuario o falta el atributo id_usersession'}), 404
        

        # Crear la instancia de User con el ID generado
        cedula_prueba = UserModel.get_user(cedula)
        if cedula_prueba is not None:
           return jsonify({'message':'La cedula ya existe'}),409
        #user.id = str(id)
        
        user = Users(str(id_user), nombre_completo, cedula, telefono,foto_perfil,huella,delante_cedula,reverso_cedula,user_session_id)
        # Agregar el usuario a la base de datos
        affected_rows = UserModel.add_user(user)
        print(affected_rows)
            

        if affected_rows != 1:
            return user.to_JSON()
        else:
                
            return jsonify({'message': "Error on insert"}), 500
        
    except Exception as ex:
        print("Estoy en ex")
        return jsonify({'message': str(ex)}), 500

@main.route('', methods=['POST'])
>>>>>>> 0bfb0d1a0a342ddc365938dc9defbf9418d4dd64
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

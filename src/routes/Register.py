#Register.py
from flask import Blueprint, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

import uuid

from models.entities.User import User
from models.UserModel import UserModel

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

main = Blueprint("register_blueprint", __name__)

@main.route('', methods=['POST'])
def add_user():
    try:
        # Generar un ID único para el usuario
        id = uuid.uuid4()

        # Obtener datos del formulario
        username = request.json['name']
        password = request.json['password']
        nombre_completo = request.json['nombre_completo']
        cedula = request.json['cedula']
        telefono = int(request.json['telefono'])
        huella = request.json['fingerprint']
        foto_perfil = request.json['profilePhoto']
        default_role = "usuario"
        delante_cedula =request.json['delante_cedula']
        reverso_cedula = request.json['reverso_cedula']

        '''cedula_prueba = UserModel.get_user(cedula)'''
        cedula_prueba = UserModel.get_user(cedula)
        if cedula_prueba is not None:
           return jsonify({'message':'La cedula ya existe'}),409
        # Crear la instancia de User con el ID generado
        #user.id = str(id)
        user = User(str(id), username, password, nombre_completo, cedula, telefono,foto_perfil,huella,default_role,delante_cedula,reverso_cedula)
        # Agregar el usuario a la base de datos
        affected_rows = UserModel.add_user(user)
        print(affected_rows)
            

        if affected_rows != 1:
            return user.to_JSON()
        else:
                
            return jsonify({'message': "Error on insert"}), 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

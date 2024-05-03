#User.py
from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import get_jwt_identity, jwt_required
import uuid

from models.entities.User import UserSession,Users

from models.UserModel import UserModel

main = Blueprint("user_blueprint", __name__)

@main.route('')
@jwt_required(optional=True)
def get_users():

    try:
        current_user_id = get_jwt_identity()
        user = UserModel.get_user_by_id(current_user_id)
        current_user_role = user['rol']
        if current_user_role == "administrador":
            users = UserModel.get_users()
            return jsonify(users)
        else:
            return jsonify({'message': "Unauthorize"}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('<cedula>')
@jwt_required(optional=True)
def get_user(cedula):

    try:
        user = UserModel.get_user(cedula)
        if user != None:
            return jsonify(user)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('add', methods=['POST'])
@jwt_required(optional=True)
def add_user():

    try:
        current_user_id = get_jwt_identity()
        user = UserModel.get_user_by_id(current_user_id)
        current_user_role = user['rol']

        if current_user_role == "administrador":

            nombre_completo = request.json['nombre_completo']
            cedula = request.json['cedula']
            telefono = int(request.json['telefono'])
            huella = request.json['fingerprint']
            foto_perfil = request.json['profilePhoto']
            delante_cedula =request.json['delante_cedula']
            reverso_cedula = request.json['reverso_cedula']
            user_session_id = session.get('user_id')  # Ejemplo, asumiendo que tienes el ID de usuario almacenado en la sesión
            
            id_user = uuid.uuid4()
            user = Users(str(id_user),nombre_completo,
                        cedula, telefono, foto_perfil, huella,delante_cedula,reverso_cedula,user_session_id)
            affected_rows = UserModel.add_user(user)

            if affected_rows == 1:
                return user.to_JSON()
            else:
                return jsonify({'message': "Error on insert"}), 500
        else:
            return jsonify({'message': "Unauthorize"}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('update_session/<id>', methods=['PUT'])
@jwt_required(optional=True)
def update_user_session(id):
    try:
        user_kw=request.json
        
        affected_rows = UserModel.update_user_session(id,**user_kw)
        print(affected_rows)
        if affected_rows != 0:
            return jsonify({"message":"Modificacion"'''user.cedula'''}),200
        else:
            return jsonify({'message': "No user updated"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('update_user/<id>', methods=['PUT'])
@jwt_required(optional=True)
def update_user(id):
    #este debe tener el toquen para poder actualizarlo
    try:
        
            user_kw=request.json
            
            affected_rows = UserModel.update_user(id,**user_kw)
            print(affected_rows)
            if affected_rows != 0:
                return jsonify({"message":"Modificacion"'''user.cedula'''}),200
            else:
                return jsonify({'message': "No user updated"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('delete/<id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_user(id):
    try:
        user = Users(id)

        affected_rows = UserModel.delete_user(user)

        if affected_rows != 1:
            return jsonify(user.id)
        else:
            return jsonify({'message': "No user deleted"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

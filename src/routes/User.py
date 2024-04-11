from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import uuid

from models.entities.User import User

from models.UserModel import UserModel

main = Blueprint("user_blueprint", __name__)


@main.route('/')
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def add_user():

    try:

        current_user_id = get_jwt_identity()
        user = UserModel.get_user_by_id(current_user_id)
        current_user_role = user['rol']

        if current_user_role == "administrador":

            username = request.json['name']
            password = request.json['password']
            nombre_completo = request.json['nombre_completo']
            cedula = request.json['cedula']
            telefono = int(request.json['telefono'])
            huella = request.json['fingerprint']
            foto_perfil = request.json['profilePhoto']
            default_role = "usuario"

            id = uuid.uuid4()
            user = User(str(id), username, password, nombre_completo,
                        cedula, telefono, foto_perfil, huella, default_role)

            affected_rows = UserModel.add_user(user)

            if affected_rows == 1:
                return user.to_JSON()
            else:
                return jsonify({'message': "Error on insert"}), 500
        else:
            return jsonify({'message': "Unauthorize"}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('update/<id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    try:
        username = request.json['name']
        password = request.json['password']
        nombre_completo = request.json['nombre_completo']
        cedula = request.json['cedula']
        telefono = int(request.json['telefono'])
        huella = request.json['fingerprint']
        foto_perfil = request.json['profilePhoto']
        rol = request.json['rol']

        user = User(id, username, password, nombre_completo,
                    cedula, telefono, foto_perfil, huella,rol)

        affected_rows = UserModel.update_user(user)

        if affected_rows == 1:
            return jsonify(user.cedula)
        else:
            return jsonify({'message': "No user updated"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('delete/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    try:
        user = User(id)

        affected_rows = UserModel.delete_user(user)

        if affected_rows == 1:
            return jsonify(user.id)
        else:
            return jsonify({'message': "No user deleted"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

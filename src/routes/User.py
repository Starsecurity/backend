# User.py
from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import get_jwt_identity, jwt_required
import uuid

from models.entities.User import UserSession, Users

from models.UserModel import UserModel
from service.IaModel import IaModel

main = Blueprint("user_blueprint", __name__)


@main.route('')
@jwt_required(optional=True)
def get_users():

    try:
        # current_user_id = get_jwt_identity()
        # user = UserModel.get_user_by_id(current_user_id)
        # current_user_role = user['rol']
        # if current_user_role == "administrador":
        users = UserModel.get_users()
        return jsonify(users)
        # else:
        #     return jsonify({'message': "Unauthorize"}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('get_relacionated_users/<id>', methods=['GET'])
@jwt_required(optional=True)
def get_users_realationated(id):
    try:
        users = UserModel.get_relationated_users(id)
        if users == None:
            return jsonify({"message": "No se encontraron usuarios registrados"}), 404
        return jsonify(users)
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
            return jsonify({"message": "No se encontro el usuario"}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('update_session/<id>', methods=['PUT'])
@jwt_required(optional=True)
def update_user_session(id):
    try:
        user_kw = request.json

        affected_rows = UserModel.update_user_session(id, **user_kw)
        print(affected_rows)
        if affected_rows != 0:
            return jsonify({"message": "Modificacion"'''user.cedula'''}), 200
        else:
            return jsonify({'message': "No user updated"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('update_user/<id>', methods=['PUT'])
@jwt_required(optional=True)
def update_user(id):
    # este debe tener el toquen para poder actualizarlo
    try:

        user_kw = request.json

        affected_rows = UserModel.update_user(id, **user_kw)
        print(affected_rows)
        if affected_rows != 0:
            return jsonify({"message": "Modificacion"}), 200
        else:
            return jsonify({'message': "No user updated"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('delete_session/<id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_user_session(id):
    try:
        # Obtener el usuario de la base de datos
        # Mirar como hacer para que solo el administrador pueda borrar las sesiones
        user = UserModel.get_user_by_id_Session(id)

        # Verificar si el usuario existe
        if user:
            # Eliminar el usuario de la base de datos
            affected_rows = UserModel.delete_user(id)

            # Verificar si se eliminó correctamente
            if affected_rows == 1:
                return jsonify({'message': "User deleted"}), 200
            else:
                return jsonify({'message': "No user deleted"}), 404
        else:
            return jsonify({'message': "User not found"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('delete_user/<id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_user(id):
    # Requiere el toquen
    try:
        
        user = UserModel.get_user_by_id(id)

        affected_rows = UserModel.delete_user(user)

        if affected_rows != 1:
            return jsonify(user.id_user)
        else:
            return jsonify({'message': "No user deleted"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('adduser/<id>', methods=['POST'])
@jwt_required(optional=True)
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
        delante_cedula = request.json['delante_cedula']
        reverso_cedula = request.json['reverso_cedula']
        fiabilidad = "Falta verificar"
        
        #validaciones de los datos
        if nombre_completo == None or cedula == None or telefono == None or huella == None or foto_perfil == None or delante_cedula == None or reverso_cedula == None:
            return jsonify({'message': 'Faltan datos'}), 404
        
        # try:
        #     stat3, selfie = IaModel.transforma_en_imagen(foto_perfil)
        #     stat4, fron_id = IaModel.transforma_en_imagen(delante_cedula)
        #     IaModel.comparar_rostros(selfie, fron_id)
        # except ValueError as e:
        #     return jsonify({'message': "Las fotos tomadas no son validas, por favor repita las fotos", 'error': str(e)}),404
        
        user_session = UserModel.get_user_by_id_Session(id)

        if user_session:
            user_session_id = user_session.get('id')
        else:
            return jsonify({'message': 'No se pudo encontrar el usuario o falta el atributo id_usersession'}), 404

        # Crear la instancia de User con el ID generado
        cedula_prueba = UserModel.get_user(cedula)
        if cedula_prueba is not None:
            return jsonify({'message': 'La cedula ya existe'}), 409
        # user.id = str(id)

        user = Users(str(id_user), nombre_completo, cedula, telefono,
                     foto_perfil, huella, delante_cedula, reverso_cedula, user_session_id, fiabilidad)
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

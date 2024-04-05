from flask import Blueprint, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import uuid

from models.entities.User import User
from models.UserModel import UserModel

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

main = Blueprint("register_blueprint", __name__)

@main.route('/', methods=['POST'])
def add_user():
    try:
        # Obtener datos del formulario
        username = request.json['username']
        password = request.json['password']
        nombre_completo = request.json['nombre_completo']
        cedula = request.json['cedula']
        telefono = int(request.json['telefono'])
        huella = request.json['huella']
        foto_perfil = request.files['foto_perfil']

        id = uuid.uuid4()
        user = User(str(id), username, password, nombre_completo, cedula, telefono,foto_perfil,huella)
        
        affected_rows = UserModel.add_user(user)

        if affected_rows == 1:
            return user.to_JSON()
        else:
            return jsonify({'message': "Error on insert"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
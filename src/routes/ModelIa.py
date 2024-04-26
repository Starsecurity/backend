import cv2
from flask import Blueprint, jsonify, request
from models.AuthModel import AuthModel
from models.UserModel import UserModel
from models.entities.User import User
from service.IaModel import IaModel
from flask_jwt_extended import jwt_required

main = Blueprint("model_blueprint", __name__)

@main.route('similarity/<id>', methods=['GET'])
@jwt_required(optional=True)
def porcentajes(id):
    try:
        
        user = UserModel.get_user_by_id(id)
        
        if user == None:
            return  jsonify({'message': "El usuario con el id no existe"}), 404
        
        print(user['fingerprint'])
        print(user['reverso_cedula'])
        huella = IaModel.transforma_en_imagen(user['fingerprint'])
        huella_cedula = IaModel.transforma_en_imagen(user['reverso_cedula'])
        similarity = IaModel.comparar_bordes(huella, huella_cedula)
        return jsonify({'porcentaje_huella':similarity})
    
    except Exception as ex:
        return  jsonify({'message': str(ex)}), 500
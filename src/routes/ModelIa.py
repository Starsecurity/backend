from flask import Blueprint, jsonify
from models.UserModel import UserModel
from service.IaModel import IaModel
from flask_jwt_extended import jwt_required

main = Blueprint("model_blueprint", __name__)

@main.route('similarity/<cedula>', methods=['GET'])
@jwt_required(optional=True)
def porcentajes(cedula):
    try:
        user = UserModel.get_user(cedula)
        
        if user == None:
            return  jsonify({'message': "El usuario con la cedula no existe"}), 404
        
        huella = IaModel.transforma_en_imagen(user['fingerprint'])
        huella_cedula = IaModel.transforma_en_imagen(user['reverso_cedula'])
        
        similarity = IaModel.comparar_bordes(huella, huella_cedula)
        return jsonify({'porcentaje_huella':similarity})
    
    except Exception as ex:
        return  jsonify({'message': str(ex)}), 500
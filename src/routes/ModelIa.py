import cv2
from flask import Blueprint, jsonify, request
from models.AuthModel import AuthModel
from models.entities.User import User
from service import IaModel
from flask_jwt_extended import jwt_required

main = Blueprint("model_blueprint", __name__)

@main.route('/similitud', methods=['POST'])
@jwt_required(optional=True)
def porcentajes():
    try:
        huella = request.json['fingerprint']
        huella_cedula = request.json['inverso_cedula']
        similarity = IaModel.comparar_bordes(huella, huella_cedula)
        return jsonify({'porcentaje_huella':similarity})
    except Exception as ex:
        return  jsonify({'message': str(ex)}), 500


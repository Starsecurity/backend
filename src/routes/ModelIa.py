from flask import Blueprint, jsonify
from models.UserModel import UserModel
from service.IaModel import IaModel
from service.resolve_captcha import VerificacionAntecedentes
from service.comprobacion import Comprobacion
from flask_jwt_extended import jwt_required

main = Blueprint("model_blueprint", __name__)


@main.route('similarity/<cedula>', methods=['GET'])
@jwt_required(optional=True)
def porcentajes(cedula):
    # Utilizar el modelo entrenado para comparar rostros
    try:
        verificacion_judicial = VerificacionAntecedentes()
        comprobacion = Comprobacion()

        nombre, numero_id, antecedentes = verificacion_judicial.get_judicial_data(
            cedula)

        if nombre == None:
            return jsonify({'message': 'El id del usuario proporcionado no es valido'}), 404

        user = UserModel.get_user(cedula)
        
        if user == None:
            return jsonify({'message': "El usuario con el id no existe"}), 404
        
        id_user = user['id']
        huella = IaModel.transforma_en_imagen(user['fingerprint'])
        huella_cedula = IaModel.transforma_en_imagen(user['reverso_cedula'])
        foto_perfil = IaModel.transforma_en_imagen(user['profilePhoto'])
        delante_cedula = IaModel.transforma_en_imagen(user['delante_cedula'])

        compatibility_percentage = IaModel.comparar_rostros(
            foto_perfil, delante_cedula)
        similarity = IaModel.comparar_bordes(huella, huella_cedula)
        
        resultado = comprobacion.comprobar_fiabilidad(
             compatibility_percentage, similarity, nombre, numero_id, antecedentes)
        
        query = UserModel.update_user(id_user, fiabilidad = resultado)
        
        if query == None:
            return jsonify({'message': 'El id del usuario proporcionado no es valido'}), 404

        return jsonify({'porcentaje_huella': similarity,
                        'porcentaje_rostro': compatibility_percentage,
                        'nombre': nombre,
                        'cedula': numero_id,
                        'antecedentesJudiciales': antecedentes,
                        'fiabilidad':resultado})

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('antecedentes/<cedula>', methods=['GET'])
@jwt_required(optional=True)
def judicial_data(cedula):
    try:
        verificacion_judicial = VerificacionAntecedentes()
        nombre, numero_id, antecedentes = verificacion_judicial.get_judicial_data(
            cedula)
        if nombre == None:
            return jsonify({'message': 'El id del usuario proporcionado no es valido'}), 404

        user = UserModel.get_user(cedula)

        if user == None:
            return jsonify({'message': "El usuario con el id no existe"}), 404

        return jsonify({'nombre': nombre,
                        'cedula': numero_id,
                        'antecedentes': antecedentes})

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

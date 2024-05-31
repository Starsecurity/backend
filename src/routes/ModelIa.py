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
        #Instancia las clases necesarias
        verificacion_judicial = VerificacionAntecedentes()
        comprobacion = Comprobacion()

        #Obtiene los datos judiciales
        nombre, numero_id, antecedentes = verificacion_judicial.get_judicial_data(
            cedula)

        #Si no se encuentra el usuario retorna un mensaje de error
        if nombre == None:
            return jsonify({'message': 'El id del usuario proporcionado no es valido'}), 404

        #Obtiene los datos del usuario
        user = UserModel.get_user(cedula)
        
        #Si no se encuentra el usuario retorna un mensaje de error
        if user == None:
            return jsonify({'message': "El usuario con el id no existe"}), 404
        
        #Obtiene los datos necesarios para la comparación
        id_user = user['id']
        
        status, huella = IaModel.transforma_en_imagen(user['fingerprint'])
        status, huella_cedula = IaModel.transforma_en_imagen(user['reverso_cedula'])
        status, foto_perfil = IaModel.transforma_en_imagen(user['profilePhoto'])
        status, delante_cedula = IaModel.transforma_en_imagen(user['delante_cedula'])
        
        #si alguna de las fotos transformadas es None retorna un mensaje de error
        if status  == False:
            return jsonify({'message': 'Error al transformar las imagenes, el url no es valido'}), 404
        
        #Realiza la comparación de los rostros y las huellas
        compatibility_percentage = IaModel.comparar_rostros(
            foto_perfil, delante_cedula)
        similarity = IaModel.comparar_bordes(huella, huella_cedula)
        
        #Obtiene el resultado de la comprobación
        resultado = comprobacion.comprobar_fiabilidad(
             compatibility_percentage, similarity, nombre, numero_id, antecedentes)
        
        #Actualiza la fiabilidad del usuario
        query = UserModel.update_user(id_user, fiabilidad = resultado)
        
        if query == None:
            return jsonify({'message': 'El id del usuario proporcionado no es valido'}), 404

        return jsonify({'porcentaje_huella': similarity,
                        'porcentaje_rostro': compatibility_percentage,
                        'nombre': nombre,
                        'cedula': numero_id,
                        'antecedentesJudiciales': antecedentes,
                        'fiabilidad':resultado,
                        'nombre_bd': user['nombre_completo']})

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

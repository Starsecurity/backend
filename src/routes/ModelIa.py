import cv2
from flask import Blueprint, jsonify,request

from models.UserModel import UserModel
from models.AuthModel import AuthModel
from models.entities.User import User
from service.IaModel import IaModel
from flask_jwt_extended import jwt_required

main = Blueprint("model_blueprint", __name__)

@main.route('/similarity/<id>', methods=['POST'])
@jwt_required(optional=True)
def porcentajes(id):
    # Utilizar el modelo entrenado para comparar rostros    

    try:
        
        user = UserModel.get_user_by_id(id)
        

        if user == None:
            return  jsonify({'message': "El usuario con el id no existe"}), 404
        
        print(user['fingerprint'])
        print(user['reverso_cedula'])
        huella = IaModel.transforma_en_imagen(user['fingerprint'])
        huella_cedula = IaModel.transforma_en_imagen(user['reverso_cedula'])
        foto_perfil = IaModel.transforma_en_imagen(user['profilePhoto'])
        foto_cedula = IaModel.transforma_en_imagen(user['delante_cedula'])

        
        
        ''' Imagenes_entrenar = [cv2.imread('C:\\Users\\JHOJAN\\Desktop\\UNICAUCA\\UNICAUCA LAB_IV ELECTRONICA\\Back_Reconocimiento\\backend\\src\\service\\Entrenamiento\\imagen1.jpg'),
                             cv2.imread('C:\\Users\\JHOJAN\\Desktop\\UNICAUCA\\UNICAUCA LAB_IV ELECTRONICA\\Back_Reconocimiento\\backend\\src\\service\\Entrenamiento\\imagen2.jpg')]
        modelo = IaModel.entrenar_modelo(Imagenes_entrenar)'''
        
            # Mostrar las imágenes con los rectángulos dibujados
        '''cv2.imshow('Rostros en la primera imagen', foto_cedula)
        cv2.imshow('Rostros en la segunda imagen', foto_perfil)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''

        compatibility_percentage= IaModel.comparar_rostros(foto_perfil,foto_cedula)
        similarity = IaModel.comparar_bordes(huella, huella_cedula)
        return jsonify({'porcentaje_huella':similarity,
                        'porcentaje_rostro':compatibility_percentage})
    
    except Exception as ex:
        return  jsonify({'message': str(ex)}), 500




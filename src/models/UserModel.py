from sqlalchemy.exc import IntegrityError
from flask import jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from database.db import session

from .entities.User import User


class UserModel():

    @classmethod
    def get_users(cls):
        try:
            users = session.query(User).all()
            return [user.to_JSON() for user in users]
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_user_by_id(cls, id):
        try:
            user = session.query(User).get(id)
            return user.to_JSON() if user else None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user(cls, cedula):
       

        try:
            user = session.query(User).filter_by(cedula=cedula).first()
            return user.to_JSON() if user else None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user(cls, user):

        try:
                session.add(user)
                session.commit()
                return user.to_JSON()
        except Exception as ex:
            session.rollback()
            print(ex)
            raise Exception(ex)
    @classmethod

    def update_user(cls, id, **kwargs):
        try:
            query = session.query(User)
            user_db = query.filter(User.id == id).first()
            if user_db:

                for key, value in kwargs.items():
                    # Verifica si el campo existe en el objeto de usuario y actualízalo
                    if hasattr(user_db, key) is not None:
                        setattr(user_db, key, value)

                session.commit()
                updated_user = session.query(User).filter(User.id == id).first()
                return updated_user.to_JSON()

            else:
                return None
        except Exception as ex:
            session.rollback()
            raise Exception(ex)

    # @classmethod
    # def update_user(cls, user):
    #     try:
    #         connection = get_connection()
    #         with connection.cursor() as cursor:
    #             # Inicializamos las partes de la consulta SQL
    #             update_query = "UPDATE usuarios SET "
    #             parameters = {}
    #             # Construimos dinámicamente la parte SET de la consulta SQL y los parámetros
    #             if user.username is not None:
    #                 update_query += "username = %s, "
    #                 parameters['username'] = user.username
    #             if user.password is not None:
    #                 update_query += "password = %s, "
    #                 parameters['password'] = generate_password_hash(
    #                     user.password)
    #             if user.nombre_completo is not None:
    #                 update_query += "nombre_completo = %s, "
    #                 parameters['nombre_completo'] = user.nombre_completo
    #             if user.cedula is not None:
    #                 update_query += "cedula = %s, "
    #                 parameters['cedula'] = user.cedula
    #             if user.telefono is not None:
    #                 update_query += "telefono = %s, "
    #                 parameters['telefono'] = user.telefono
    #             if user.foto_perfil is not None:
    #                 update_query += "foto_perfil = %s, "
    #                 parameters['foto_perfil'] = user.foto_perfil
    #             if user.huella is not None:
    #                 update_query += "huella = %s, "
    #                 parameters['huella'] = user.huella
    #             # Verificamos si hay campos para actualizar
    #             if parameters:
    #                 update_query = update_query.rstrip(
    #                     ', ')  # Elimina la coma final
    #                 update_query += " WHERE id = %s"
    #                 parameters['id'] = user.id
    #                 cursor.execute(update_query, list(parameters.values()))
    #                 affected_rows = cursor.rowcount
    #                 connection.commit()
    #             else:
    #                 # Si no hay campos para actualizar, retornamos 0 filas afectadas
    #                 affected_rows = 0
    #         connection.close()
    #         return affected_rows
    #     except Exception as ex:
    #         raise Exception(ex)

    @classmethod
    def delete_user(cls, user):
        try:
            user = session.query(User).get(id)
            if user:
                session.delete(user)
                session.commit()
                return id
            else:
                return None
        except Exception as ex:
            session.rollback()
            raise Exception(ex)

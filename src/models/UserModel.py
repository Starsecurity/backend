from flask import jsonify
from flask_jwt_extended import create_access_token
from database.db import get_connection
from werkzeug.security import generate_password_hash

from .entities.User import User


class UserModel():

    @classmethod
    def get_users(self):
        try:
            connection = get_connection()
            users = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM usuarios")
                resultset = cursor.fetchall()
                
                for row in resultset:
                    user = User(row[0], row[1], row[2], row[3],
                                row[4], row[5], row[6], row[7], row[8])
                    users.append(user.to_JSON())

            connection.close()
            return users
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user_by_id(self, id):
        try:
            connection = get_connection()
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM usuarios WHERE id = %s", (id,))
                row = cursor.fetchone()
                
                user = None
                if row != None:
                    user = User(row[0], row[1], row[2], row[3],
                                row[4], row[5], row[6], row[7], row[8])
                    user = user.to_JSON()

            connection.close()
            return user
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_user(self, cedula):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM usuarios WHERE cedula = %s", (cedula,))
                row = cursor.fetchone()

                user = None
                if row != None:
                    user = User(row[0], row[1], row[2], row[3],
                                row[4], row[5], row[6], row[7], row[8])
                    user = user.to_JSON()

            connection.close()
            return user
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user(self, user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO usuarios (id, username, password, nombre_completo, cedula, telefono, foto_perfil, huella,rol) 
                                VALUES (%s,%s, %s, %s, %s,%s,%s,%s,%s)""", (user.id, user.username, generate_password_hash(user.password), user.nombre_completo, user.cedula, user.telefono, user.foto_perfil, user.huella, user.rol))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_user(self, user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE usuarios SET username = %s, password = %s , nombre_completo = %s, cedula = %s, telefono = %s, foto_perfil = %s,huella = %s, rol=%s WHERE id = %s""", (
                    user.username, generate_password_hash(user.password), user.nombre_completo,  user.cedula, user.telefono, user.foto_perfil, user.huella,user.rol, user.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
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
    def delete_user(self, user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM usuarios WHERE id = %s", (user.id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

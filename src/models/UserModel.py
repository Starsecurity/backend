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
                    "SELECT id, username, password, nombre_completo, cedula, telefono, foto_perfil, huella FROM usuarios")
                resultset = cursor.fetchall()

                for row in resultset:
                    user = User(row[0], row[1], row[2], row[3], row[4], row[5])
                    users.append(user.to_JSON())

            connection.close()
            return users
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user(self, cedula):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, password, nombre_completo, cedula, telefono, foto_perfil, huella FROM usuarios WHERE cedula = %s", (cedula,))
                row = cursor.fetchone()

                user = None
                if row != None:
                    user = User(row[0], row[1], row[2], row[3], row[4], row[5])
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
                cursor.execute("""INSERT INTO usuarios (id, username, password, nombre_completo, cedula, telefono, foto_perfil, huella) 
                                VALUES (%s,%s, %s, %s, %s,%s,%s,%s)""", (user.id,user.username, generate_password_hash(user.password), user.nombre_completo, user.cedula, user.telefono,user.foto_perfil,user.huella))
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
                cursor.execute("""UPDATE usuarios SET username = %s, password = %s , nombre_completo = %s, cedula = %s, telefono = %s,  WHERE id = %s""", (
                     user.username, generate_password_hash(user.password), user.nombre_completo,  user.cedula,user.telefono, user.foto_perfil, user.huela ,user.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_user(self, user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (user.id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    # @classmethod
    # def login(self, user):
    #     try:
    #         cursor = get_connection().cursor()
    #         sql = """SELECT id, username, password, nombre_completo, cedula, telefono FROM usuarios 
    #                 WHERE username = '{}'""".format(user.username)
    #         cursor.execute(sql)
    #         row = cursor.fetchone()
    #         if row != None:
    #             user = User(row[0], row[1], User.check_password(
    #                 row[2], user.password), row[3], row[4], row[5])
                
    #             access_token = create_access_token(identity = user.id)
    #             user = user.to_JSON()
                
    #             return jsonify({'token':access_token,'user':user})
    #         else:
    #             return None
    #     except Exception as ex:
    #         raise Exception(ex)

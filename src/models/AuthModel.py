from flask import jsonify
from flask_jwt_extended import create_access_token
from database.db import get_connection
from .entities.User import User


class AuthModel():

    @classmethod
    def login(self, user):
        try:
            cursor = get_connection().cursor()
            sql = """SELECT * FROM usuarios
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(
                    row[2], user.password), row[3], row[4], row[5],row[6],row[7],row[8],row[9],row[10])

                access_token = create_access_token(identity=user.id)
                user = user.to_JSON()
                
                return jsonify({'token': access_token, 'user': user})
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def user_role(self, user):
        try:
            cursor = get_connection().cursor()
            sql = """SELECT * FROM usuarios 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row != None:
                role = User(user.rol)
                return jsonify({'rol': role})
            else:
                return None, 400
        except Exception as ex:
            raise Exception(ex)
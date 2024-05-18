from sqlalchemy.exc import IntegrityError
from flask import jsonify
from database.db import session
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

from .entities.User import UserSession, Users


class UserModel():
    @classmethod
    def get_users(cls):
        try:
            users = session.query(Users).all()
            return [user.to_JSON() for user in users]
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user_by_id(cls, id):
        try:
            user = session.query(Users).get(id)
            return user.to_JSON() if user else None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_relationated_users(cls, id):
        try:
            users = session.query(Users).filter_by(user_session_id=id).all()
            return [user.to_JSON() for user in users]
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user(cls, cedula):

        try:
            user = session.query(Users).filter_by(cedula=cedula).first()
            return user.to_JSON() if user else None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user_username(cls, username):

        try:
            user = session.query(UserSession).filter_by(
                username=username).first()
            return user.to_JSON_session() if user else None
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
            raise Exception(ex)

    @classmethod
    def update_user(cls, id, **kwargs):
        try:
            query = session.query(Users)
            user_db = query.filter(Users.id_user == id).first()
            if user_db:

                for key, value in kwargs.items():
                    # Verifica si el campo existe en el objeto de usuario y actualízalo
                    if hasattr(user_db, key) is not None:
                        setattr(user_db, key, value)

                session.commit()
                updated_user = session.query(Users).filter(
                    Users.id_user == id).first()
                return updated_user.to_JSON()

            else:
                return None
        except Exception as ex:
            print("Estoy en ex")
            raise Exception(ex)

    @classmethod
    def delete_user(cls, user):
        try:
            user = session.query(Users).get(id)
            if user:
                session.delete(user)
                session.commit()
                return id
            else:
                return None
        except Exception as ex:
            session.rollback()
            raise Exception(ex)

    @classmethod
    def get_users_session(cls):
        try:
            users = session.query(UserSession).all()
            return [user.to_JSON_session() for user in users]
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user_by_id_Session(cls, id):
        try:
            user = session.query(UserSession).get(id)
            return user.to_JSON_session() if user else None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user_session(cls, user):

        try:
            session.add(user)
            session.commit()
            return user.to_JSON_session()
        except Exception as ex:
            session.rollback()
            raise Exception(ex)

    @classmethod
    def update_user_session(cls, id, **kwargs):
        try:
            query = session.query(UserSession)
            user_db = query.filter(UserSession.id == id).first()
            print(user_db.id)
            if user_db:

                for key, value in kwargs.items():
                    # Verifica si el campo existe en el objeto de usuario y actualízalo
                    if hasattr(user_db, key) is not None:
                        setattr(user_db, key, value)

                session.commit()
                updated_user = session.query(UserSession).filter(
                    UserSession.id == id).first()
                return updated_user.to_JSON_session()

            else:
                return None
        except Exception as ex:
            print("Estoy en ex")
            session.rollback()
            raise Exception(ex)

    @classmethod
    def delete_user_session(cls, id):
        try:
            user = session.query(UserSession).get(id)
            if user:
                session.delete(user)
                session.commit()
                return user.id
            else:
                return None
        except Exception as ex:
            session.rollback()
            raise Exception(ex)

    @classmethod
    def delete_user(cls, user):
        # Debe tener el token
        try:
            user = session.query(Users).get(id)
            if user:
                session.delete(user)
                session.commit()
                return id
            else:
                return None
        except Exception as ex:
            session.rollback()
            raise Exception(ex)

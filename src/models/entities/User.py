from flask import session
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash

Base = declarative_base()

class RolEnum(Enum):
    ADMINISTRADOR = 'administrador'
    USUARIO = 'usuario'

class Users(Base):
    __tablename__='users'
    id_user = Column(String, primary_key=True)
    nombre_completo = Column(String, nullable=False)   
    cedula = Column(String, nullable=False)  # Puedes agregar 'unique=True' aquí si deseas
    telefono = Column(String, nullable=False) 
    foto_perfil = Column(String, nullable=True)
    huella = Column(String, nullable=True)
    delante_cedula = Column(String,nullable=True)
    reverso_cedula = Column(String,nullable=True)
    user_session_id=Column(String,ForeignKey('usersession.id'))

    def __init__(self, id, nombre_completo, cedula, telefono, foto_perfil, huella,delante_cedula,reverso_cedula,user_session_id):
        self.id_user=id
        self.nombre_completo = nombre_completo
        self.cedula = cedula
        self.telefono = telefono
        self.foto_perfil = foto_perfil
        self.huella = huella
        self.delante_cedula=delante_cedula
        self.reverso_cedula=reverso_cedula
        self.user_session_id=user_session_id


    def to_JSON(self):
        return {
            'id': self.id_user,
            'nombre_completo': self.nombre_completo,
            'cedula': self.cedula,
            'telefono': self.telefono,
            'profilePhoto': self.foto_perfil,
            'fingerprint': self.huella,
            'delante_cedula':self.delante_cedula,
            'reverso_cedula':self.reverso_cedula,
            'user_session_id':self.user_session_id
        }

class UserSession(Base):
    __tablename__='usersession'
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False) 
    correo=Column(String,nullable=False)
    rol = Column(Enum('usuario', 'administrador', name='rol_enum'), nullable=False)

    def __init__(self, id,username, password, correo,rol):
        self.id=id
        self.username = username
        self.password = password
        self.correo= correo
        self.rol = rol



    def to_JSON_session(self):
        return {
            'id': self.id,
            'name': self.username,
            'password': self.password,
            'correo':self.correo,
            'rol': self.rol
        }

    def check_password(self, password):
        return check_password_hash(self.password, password)


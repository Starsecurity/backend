from flask import session
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash

Base = declarative_base()

class RolEnum(Enum):
    ADMINISTRADOR = 'administrador'
    USUARIO = 'usuario'

class User(Base):
    __tablename__='usuarios'
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    nombre_completo = Column(String, nullable=False)   
    cedula = Column(String, nullable=False)  # Puedes agregar 'unique=True' aquí si deseas
    telefono = Column(Integer, nullable=False) 
    foto_perfil = Column(String, nullable=True)
    huella = Column(String, nullable=True)
    rol = Column(Enum('usuario', 'administrador', name='rol_enum'), nullable=False)
    delante_cedula = Column(String, nullable=True)
    reverso_cedula = Column(String, nullable=True)
    
    def __init__(self, id,username, password, nombre_completo, cedula, telefono, foto_perfil, huella, rol,delante_cedula,reverso_cedula):
        self.id=id
        self.username = username
        self.password = password
        self.nombre_completo = nombre_completo
        self.cedula = cedula
        self.telefono = telefono
        self.foto_perfil = foto_perfil
        self.huella = huella
        self.rol = rol
        self.delante_cedula = delante_cedula
        self.reverso_cedula = reverso_cedula

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.username,
            'password': self.password,
            'nombre_completo': self.nombre_completo,
            'cedula': self.cedula,
            'telefono': self.telefono,
            'profilePhoto': self.foto_perfil,
            'fingerprint': self.huella,
            'rol': self.rol,
            'delante_cedula' : self.delante_cedula,
            'reverso_cedula' : self.reverso_cedula
        }

    def check_password(self, password):
        return check_password_hash(self.password, password)


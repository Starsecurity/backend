from werkzeug.security import check_password_hash

class User():

    def __init__(self, id, username=None, password = None, nombre_completo = None, cedula = None, telefono = None) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.nombre_completo = nombre_completo
        self.cedula = cedula
        self.telefono = telefono

    def to_JSON(self):
        return {
            'id' :  self.id,
            'username' : self.username,
            'password' :  self.password,
            'nombre_completo' :  self.nombre_completo,
            'cedula' :  self.cedula,
            'telefono' : self.telefono
        }
    
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
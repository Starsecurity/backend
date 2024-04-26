from werkzeug.security import check_password_hash

class User():

    def __init__(self, id, username=None, password = None, nombre_completo = None, cedula = None, telefono = None, foto_perfil = None, huella = None, rol = None, delante_cedula = None, reverso_cedula = None) -> None:
        self.id = id
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
            'id' :  self.id,
            'name' : self.username,
            'password' :  self.password,
            'nombre_completo' :  self.nombre_completo,
            'cedula' :  self.cedula,
            'telefono' : self.telefono,
            'profilePhoto': self.foto_perfil,
            'fingerprint' : self.huella,
            'rol' : self.rol,
            'delante_cedula' : self.delante_cedula,
            'reverso_cedula' : self.reverso_cedula
        }
    
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
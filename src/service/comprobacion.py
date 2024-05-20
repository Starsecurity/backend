from models.UserModel import UserModel


class Comprobacion():

    def comprobar_fiabilidad(self, compatibility_percentage, similarity, nombre, numero_id, antecedentes):

        user = UserModel.get_user_by_id(numero_id)
        name_bd = user['nombre']
        # Convertir el string a mayúsculas
        uppercase_string = name_bd.upper()
        # Eliminar los espacios
        final_name = uppercase_string.replace(" ", "")
        id_bd = user['cedula']

        if compatibility_percentage < 0.6:
            return "Baja fiabilidad"
        if similarity < 0.6:
            return "Baja fiabilidad"
        if antecedentes:
            return "Baja fiabilidad"
        if nombre != final_name:
            return "Baja fiabilidad"
        if id_bd != numero_id:
            return "Baja fiabilidad"

        return "Alta fiabilidad"
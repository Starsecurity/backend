from models.UserModel import UserModel

class Comprobacion():

    def comprobar_fiabilidad(self,compatibility_percentage,similarity,nombre,numero_id,antecedentes):
        
        user = UserModel.get_user_by_id(numero_id)
        nombre_bd = user['nombre']
        cedula_bd = user['cedula']

        if compatibility_percentage < 0.5:
            return "Baja fiabilidad"
        if similarity < 0.5:
            return "Baja fiabilidad"
        if antecedentes:
            return "Baja fiabilidad"
        if nombre != nombre_bd:
            return "Baja fiabilidad"
        if cedula_bd != numero_id:
            return "Baja fiabilidad"

        return "Alta fiabilidad"
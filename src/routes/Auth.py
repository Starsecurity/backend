# 
from flask import Blueprint, jsonify, request
from models.AuthModel import AuthModel
from models.entities.User import User
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager

main = Blueprint("auth_blueprint", __name__)
@main.route('/login', methods=['POST'])
def login():
    try:
        # Obtener datos del usuario desde la solicitud JSON
        username = request.json.get('name')
        password = request.json.get('password')

        # Verificar que se hayan proporcionado tanto el nombre de usuario como la contraseña
        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400

        # Llamar a la función login de AuthModel pasando el username y password
        user_data = AuthModel.login(username, password)

        # Devolver los datos del usuario
        return user_data
    except Exception as ex:
        return  jsonify({'message': str(ex)}), 500
    
@main.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

# @api.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             data = response.get_json()
#             if type(data) is dict:
#                 data["access_token"] = access_token 
#                 response.data = json.dumps(data)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original respone
#         return response


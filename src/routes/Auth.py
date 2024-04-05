from flask import Blueprint, jsonify , request
from models.AuthModel import AuthModel
from models.entities.User import User
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager

main = Blueprint("auth_blueprint", __name__)

@main.route('/login', methods=['POST'])
def auth():
    try:
        user = User(id,request.json['username'],request.json['password'])
        user_data = AuthModel.login(user)
        return user_data
    except Exception as ex:
        return  jsonify({'message': str(ex)}), 500

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

# @main.route('/login',methods=['POST'])
#     def

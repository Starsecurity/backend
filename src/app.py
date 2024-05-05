from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import config 

from routes import Auth, User , Register, ModelIa

app = Flask(__name__)
jwt = JWTManager(app)

CORS(app,resources={"*":{"origins":"*"}})

def page_not_found(error):
    return "<h1>Not found page</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    
    app.register_blueprint(Register.main, url_prefix='/register')
    app.register_blueprint(Auth.main, url_prefix='/auth')
    app.register_blueprint(User.main, url_prefix='/api/user')
    app.register_blueprint(ModelIa.main, url_prefix='/model')
    
    app.register_error_handler(404,page_not_found)
    app.run()
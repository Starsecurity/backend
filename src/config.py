from decouple import config

class Config:
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    #JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
class DevelompentConfig(Config):
    DEBUG = True

config = {
    'development': DevelompentConfig
}

import os

SECRET_KEY = 'miau'
SQLALCHEMY_TRACK_MODIFICATIONS = False


SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'mysql',
        database = 'db'
    )


UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
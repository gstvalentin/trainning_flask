from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import inicia_db

inicia_db()
app = Flask(__name__)
app.config.from_pyfile('config.py') #import configs
db = SQLAlchemy(app) #comandos pra db
app.config['SESSION_COOKIE_HTTPONLY'] = False
from views import * #importa views

# trecho da app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py') #import configs
db = SQLAlchemy(app) #comandos pra db
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_HTTPONLY'] = False


from views import * #importa views

# trecho da app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
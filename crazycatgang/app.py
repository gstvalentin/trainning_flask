from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py') #import configs
db = SQLAlchemy(app) #conecta a db

from views import * #importa views

# trecho da app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
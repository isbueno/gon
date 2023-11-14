from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__) # Criando o app flask
app.app_context().push() # Definindo um contexto para ele

# Configurações do banco de dados - ORM
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
UPLOAD_PATH = os.environ.get('UPLOAD_PATH')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


# Importações quem devem aparecer no app (principal)
from app import routes
from app import error


if __name__ == '__main__':
    app.run()


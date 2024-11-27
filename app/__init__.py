from flask import Flask
from flask_cors import CORS
from app.database.db import init_db
from app.routes import auth

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS

    # Inicializa la base de datos
    init_db(app)

    # Registra rutas
    app.register_blueprint(auth.auth_blueprint)

    return app

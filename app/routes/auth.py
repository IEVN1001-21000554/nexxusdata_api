from flask import Blueprint, request, jsonify
from app.database.db import mysql

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    cursor = mysql.connection.cursor()
    query = "SELECT id FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({"message": "Inicio de sesión exitoso", "user_id": user[0]}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

@auth_blueprint.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validar datos
    if not username or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    cursor = mysql.connection.cursor()

    # Verificar si el usuario o correo ya existen
    check_query = "SELECT id FROM users WHERE username = %s OR email = %s"
    cursor.execute(check_query, (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        return jsonify({"error": "El usuario o correo ya están registrados"}), 409

    # Insertar nuevo usuario
    insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (username, email, password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Usuario registrado con éxito"}), 201

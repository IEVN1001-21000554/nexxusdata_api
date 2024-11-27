from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import bcrypt

# Configuración básica de la aplicación Flask
app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia según tu configuración
app.config['MYSQL_PASSWORD'] = ''  # Cambia según tu configuración
app.config['MYSQL_DB'] = 'nexxusdata'  # Nombre de tu base de datos

mysql = MySQL(app)

# Ruta de prueba
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido al backend de NexxusData"}), 200

# Ruta para registrar usuarios
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    nombre_usuario = data.get('nombre_usuario')
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    rol = data.get('rol', 'admin')  # Valor predeterminado "admin"

    hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre_usuario, correo, contraseña, rol) VALUES (%s, %s, %s, %s)",
                       (nombre_usuario, correo, hashed_password, rol))
        mysql.connection.commit()
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    correo = data.get('correo')
    contraseña = data.get('contraseña')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario and bcrypt.checkpw(contraseña.encode('utf-8'), usuario[3].encode('utf-8')):  # Índice 3 es la contraseña
        return jsonify({"message": "Inicio de sesión exitoso", "rol": usuario[4]}), 200  # Índice 4 es el rol
    return jsonify({"error": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run(debug=True)

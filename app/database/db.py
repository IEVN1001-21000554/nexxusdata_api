from flask_mysqldb import MySQL
from app.config import get_config

mysql = MySQL()

def init_db(app):
    config = get_config()

    app.config["MYSQL_HOST"] = config.DB_HOST
    app.config["MYSQL_PORT"] = config.DB_PORT
    app.config["MYSQL_USER"] = config.DB_USER
    app.config["MYSQL_PASSWORD"] = config.DB_PASSWORD
    app.config["MYSQL_DB"] = config.DB_NAME

    mysql.init_app(app)

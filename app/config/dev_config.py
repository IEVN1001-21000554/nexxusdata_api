from .base_config import BaseConfig

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DB_PASSWORD = "password_dev"  # Cambia según tu entorno de desarrollo

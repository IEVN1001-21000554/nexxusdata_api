from .base_config import BaseConfig

class ProductionConfig(BaseConfig):
    DB_PASSWORD = "password_prod"  # Cambia según tu entorno de producción

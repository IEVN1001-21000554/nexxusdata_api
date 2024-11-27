import os
from .dev_config import DevelopmentConfig
from .prod_config import ProductionConfig

def get_config():
    environment = os.getenv("FLASK_ENV", "development")  # Por defecto "development"
    if environment == "production":
        return ProductionConfig
    return DevelopmentConfig

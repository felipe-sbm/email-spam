import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{DATA_DIR / "emails.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Model paths
    MODEL_PATH = os.environ.get('MODEL_PATH') or str(BASE_DIR / 'spam_model.pkl')
    VECTORIZER_PATH = os.environ.get('VECTORIZER_PATH') or str(BASE_DIR / 'vectorizer.pkl')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

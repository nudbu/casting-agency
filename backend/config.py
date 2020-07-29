import os

# Database
database_name = "casting"
postgres_user = "postgres"
host = "localhost"
port = "5432"
database_path = f"postgresql://{postgres_user}@{host}:{port}/{database_name}"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or database_path
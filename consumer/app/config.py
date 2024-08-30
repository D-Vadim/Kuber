# Configurations for the application
import os

DATABASE = {
    'dbname': os.getenv('POSTGRES_DB', 'weather_archive'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'root456'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', 5432)
}

'''
DATABASE = {
    'dbname': 'weather_archive',
    'user': 'postgres',
    'password': 'root456',
    'host': 'localhost',
    'port': 5432,
}
'''

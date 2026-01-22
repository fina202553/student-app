import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """アプリケーション構成クラス"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST') or 'localhost',
        'database': os.environ.get('DB_NAME') or 'student_db',
        'user': os.environ.get('DB_USER') or 'postgres',
        'password': os.environ.get('DB_PASSWORD') or 'password',
        'port': os.environ.get('DB_PORT') or '5432'
    }
import os
from pathlib import Path

# Get the absolute path to the project directory
BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # Absolute path
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'doc'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'recipes.db')
SECRET_KEY = 'your-secret-key-here'
WHATSAPP_NUMBER = '255622387189'

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET', 'msosihub')  # Default to msosihub
AWS_REGION = os.environ.get('AWS_REGION', 'ap-northeast-1')
S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL', 'https://s3.ap-northeast-1.amazonaws.com')

# Additional recommended settings
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_S3_CORS = os.environ.get('AWS_S3_CORS', 'True') == 'True'  # New
AWS_S3_MAX_AGE_SECONDS = int(os.environ.get('AWS_S3_MAX_AGE_SECONDS', '3000'))  # New
S3_USE_SSL = True
S3_VERIFY = True  # Verify SSL certificates
S3_DEFAULT_ACL = 'private'  # Or 'public-read' if you want public access

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key') # Never use fallback in production!

    
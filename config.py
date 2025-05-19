# config.py
import os
from warnings import warn

class ConfigError(Exception):
    pass

# --------------------------
# Core Configuration
# --------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'

# --------------------------
# Database Configuration
# --------------------------
if os.environ.get('DATABASE_URL'):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'].replace(
        'postgres://', 'postgresql://', 1
    )
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        f'sqlite:///{os.path.join(BASE_DIR, "recipes.db")}'
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False

# --------------------------
# AWS S3 Configuration
# --------------------------
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET', 'msosihub')
AWS_REGION = os.environ.get('AWS_REGION', 'ap-northeast-1')
S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL', f'https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com')

# Security settings
AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION', 's3v4')
AWS_S3_ADDRESSING_STYLE = os.environ.get('AWS_S3_ADDRESSING_STYLE', 'virtual')
S3_USE_HTTPS = os.environ.get('S3_USE_HTTPS', 'True') == 'True'
S3_DEFAULT_ACL = os.environ.get('S3_DEFAULT_ACL', 'private')

# --------------------------
# Security Configuration
# --------------------------
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY and FLASK_ENV == 'production':
    raise ConfigError("SECRET_KEY must be set in production environment")

# --------------------------
# WhatsApp Configuration
# --------------------------
WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '255622387189')

# --------------------------
# Production Checks
# --------------------------
if FLASK_ENV == 'production':
    if DEBUG:
        warn("DEBUG mode is enabled in production!", RuntimeWarning)
    
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY]):
        raise ConfigError("AWS credentials must be set in production environment")

# --------------------------
# Additional Security Headers
# --------------------------
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_ENABLED = os.environ.get('CSRF_ENABLED', 'True') == 'True'
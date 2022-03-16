import os
from dotenv import load_dotenv
load_dotenv()

# Statement for enabling the development environment
DEBUG = True
DATABASE_PASSWORD = 'Y3A8Jvg2yGEWtyBP'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/FYPD'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = { "pool_pre_ping": True, "pool_recycle": 300 }
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

MAX_CONTENT_LENGTH = 5 * 1000 * 1000 # 5 megabytes

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET") if os.environ.get("ACCESS_TOKEN_SECRET") is not None else "access_token_development_secret"
REFRESH_TOKEN_SECRET = os.environ.get("REFRESH_TOKEN_SECRET") if os.environ.get("REFRESH_TOKEN_SECRET") is not None else "access_token_development_secret"

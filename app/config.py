# Statement for enabling the development environment
DEBUG = True
DATABASE_PASSWORD = 'ceef9ffe'
SQLALCHEMY_DATABASE_URI = f'mysql://b1af419355f3a4:{DATABASE_PASSWORD}@us-cdbr-east-05.cleardb.net/heroku_dc2cd1ae84a7237'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

import dj_database_url

from btc_backend.settings import *  # noqa: F401,F403
from btc_backend.configurations import DATABASE_URL, CORS_ALLOWED_ORIGINS_STR

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

# Served by the shared nginx container under the /btc/ location block.
STATIC_URL = '/btc/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# nginx strips the /btc prefix before forwarding, so urlpatterns stay unprefixed;
# this makes reverse()/build_absolute_uri()/pagination links re-add the prefix correctly.
FORCE_SCRIPT_NAME = '/btc'

# Required in Django 4+ when behind a reverse proxy — CSRF checks the Origin header
# against this list. Must include the full scheme + domain.
CSRF_TRUSTED_ORIGINS = ['https://api.rhoafrica.com']

# Origins allowed to make cross-site requests (comma-separated in .env)
CORS_ALLOWED_ORIGINS = [o.strip() for o in CORS_ALLOWED_ORIGINS_STR.split(',')]
CORS_ALLOW_HEADERS = [
    'accept', 'authorization', 'content-type', 'origin', 'x-csrftoken',
]

# Tell Django the real scheme/host since nginx terminates SSL.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

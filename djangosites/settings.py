DEBUG = False
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Australia/Melbourne'
LANGUAGE_CODE = 'en-AU'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = '/var/python-envs/djangosites/htdocs/'
MEDIA_URL = '/media/'
STATIC_ROOT = MEDIA_ROOT + 'static/'
STATIC_URL = MEDIA_URL + 'static/'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'djangosites.middleware.threadlocals.ThreadLocals',
    'djangosites.middleware.blockips.BlockedIpMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'djangosites.urls'

TEMPLATE_DIRS = (
    '/var/python-envs/djangosites/djangosites/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'djangosites.websites',
    'tagging',
    'voting',
    'django.contrib.markup',
    'django.contrib.humanize',
    'registration',
    'django_authopenid',
    'south',
    'memcache_status',
    'flag',
    'pagination',
    'gunicorn',
    'djrill',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
ACCOUNT_ACTIVATION_DAYS = 7

INTERNAL_IPS = (
)

PREPEND_WWW=False

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.i18n",
    "djangosites.websites.contexts.tagcloud",
    'django_authopenid.context_processors.authopenid',
)


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'djangosites',
    }
}


EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

FORCE_LOWERCASE_TAGS = True


CACHE_MIDDLEWARE_SECONDS=600
CACHE_MIDDLEWARE_KEY_PREFIX='djangosites-anonymous-cache'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True

try:
    from local_settings import *
except:
    pass

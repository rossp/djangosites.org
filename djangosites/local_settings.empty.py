# Database connection details
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangosites',
        'USER': 'username',
        'PASS': 'mypassword',
    }
}

# Django secret key, used to hash passwords etc.
# Migrated from your initial settings.py
SECRET_KEY = '' 

# Used to send email via Mandrillapp.com (Mailchimp's Transactional email provider)
MANDRILL_API_KEY='' # Taken from mandrillapp.com

# Used by admin.py to post to Twitter whenever a site is verified.
TWITTER_OAUTH_CONSUMER_KEY=''
TWITTER_OAUTH_CONSUMER_SECRET=''
TWITTER_OAUTH_ACCESS_KEY = ''
TWITTER_OAUTH_ACCESS_SECRET = ''


# Used by get_thumbs.py to generate screenshots of webpages.
# Sign up at http://webthumnb.bluga.net
WEBTHUMB_API_KEY = ''

# AWS credentials. Not currently used by any part of the live site.
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
BUCKET_NAME = ''

# Bitly API credentials
# Used to shorten links when tweeting
# http://bit.ly
BITLY_USERNAME = ''
BITLY_APIKEY = ''

# Admin email addresses for server errors
ADMINS = (
    ('Full Name', 'email@example.org'),
)
MANAGERS = ADMINS

# Settings used for outgoing emails
DEFAULT_FROM_EMAIL = 'DjangoSites <djangosites@example.org>'
DEFAULT_FROM_ADDRESS = 'DjangoSites <djangosites@example.org>'
EMAIL_SUBJECT_PREFIX = '[djangosites] '
SERVER_EMAIL='DjangoSites <djangosites@example.org>'

# Middleware is in place to block these IPs which have traditionally 
# caused me huge numbers of server errors due to incredibly poorly 
# written scrapers / bots.
BLOCKED_IPS = ('61.160.232.104', '173.192.238.48', '222.186.26.103', '117.41.185.111', '122.226.223.67', '60.169.73.207', '61.160.232.102', '61.160.232.101','60.169.73.211', '61.160.232.4', '222.186.26.155', '222.186.24.68', '174.37.205.68')

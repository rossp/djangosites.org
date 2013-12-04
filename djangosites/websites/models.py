from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from datetime import datetime

from django.db.models import signals

from voting.models import Vote

from djangosites.websites.signals import update_website_votes

from djangosites.middleware import threadlocals
from django.conf.locale import LANG_INFO

SS_CHOICES = (
    ('none', 'No Screenshot'),
    ('updating', 'Updating'),
    ('ok', 'Screenshot is OK'),
)

OS_CHOICES = (
    ('bsd', 'BSD based'),
    ('google', 'Google App Engine'),
    ('linux', 'Linux based'),
    ('osx', 'OS-X'),
    ('sun', 'Sun OS'),
    ('windows', 'Windows'),
)

DJANGO_CHOICES = (
    ('0.90', '0.90 Release'),
    ('0.91', '0.91 Release'),
    ('0.95', '0.95 Release'),
    ('0.96', '0.96 Release'),
    ('1.0', '1.0 Release'),
    ('1.1', '1.1 Release'),
    ('1.2', '1.2 Release'),
    ('1.3', '1.3 Release'),
    ('1.4', '1.4 Release'),
    ('1.5', '1.5 Release'),
    ('1.6', '1.6 Release'),
    ('stablesvn', 'A Particular Git checkout'),
    ('trunk', 'Up to date Git master'),
)

PYTHON_CHOICES = (
    ('2.3', '2.3 Release'),
    ('2.4', '2.4 Release'),
    ('2.5', '2.5 Release'),
    ('2.6', '2.6 Release'),
    ('2.7', '2.7 Release'),
    ('3.0', '3.0 Release'),
    ('3.1', '3.1 Release'),
    ('3.2', '3.2 Release'),
    ('3.3', '3.3 Release'),
    ('3.4', '3.4 Release'),
)

WEBSERVER_CHOICES = (
    ('apache', 'Apache'),
    ('cherrypy', 'CherryPy'),
    ('cherokee', 'Cherokee'),
    ('dev', 'Django Development Server'),
    ('google', 'Google App Engine'),
    ('iis', 'IIS'),
    ('lighttpd', 'LigHTTPD'),
    ('nginx', 'Nginx'),
    ('passenger', 'Passenger'),
    ('spawning', 'Spawning'),
    ('web2py', 'web2.py'),
    ('paas', 'PAAS (Heroku, GAE, Gondor, etc'),
)

DATABASE_CHOICES = (
    ('google', 'Google BigTable'),
    ('mssql', 'MS SQL Server'),
    ('mysql', 'MySQL'),
    ('oracle', 'Oracle'),
    ('postgres', 'PostgreSQL'),
    ('sqlite', 'SQLite'),
    ('redis', 'Redis'),
    ('cassandra', 'Cassandra'),
    ('couchdb', 'Apache CouchDB'),
    ('mongodb', 'MongoDB'),
)

METHOD_CHOICES = (
    ('google', 'Google App Engine'),
    ('gunicorn', 'Gunicorn'),
    ('mod_python', 'mod_python'),
    ('mod_wsgi', 'mod_wsgi'),
    ('fastcgi', 'FastCGI'),
    ('dev', 'Django Development Server'),
    ('scgi', 'Simple CGI (scgi)'),
    ('tornado', 'Tornado'),
    ('wsgi', 'wsgi'),
    ('uwsgi', 'uWSGI'),
    ('paas', 'PAAS (Heroku, GAE, Gondor, etc'),
)

LANGUAGE_CHOICES = []
for language in LANG_INFO.keys():
    LANGUAGE_CHOICES.append((LANG_INFO[language]['code'], LANG_INFO[language]['name']))


class Website(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    slug = models.SlugField(editable=False, blank=True, null=True, max_length=250)
    owner = models.ForeignKey(User, blank=True, null=True, editable=False)
    description = models.TextField()
    tags = TagField(blank=True, null=True)
    verified = models.BooleanField(blank=True, default=False, editable=False)
    created = models.DateTimeField(blank=True, null=True, editable=False)
    
    comment_count = models.IntegerField(blank=True, null=True, editable=False)
    num_votes = models.IntegerField(blank=True, null=True, editable=False)
    votes = models.IntegerField(blank=True, null=True, editable=False)

    screenshot = models.CharField(max_length=10, choices=SS_CHOICES, blank=True, null=True, editable=False)
    webthumb_key = models.CharField(max_length=100, blank=True, null=True, editable=False)

    source_url = models.URLField(blank=True, null=True)
    
    sotw_url = models.URLField(blank=True, null=True, editable=False)

    deployment_os = models.CharField(max_length=100, blank=True, null=True, choices=OS_CHOICES)
    deployment_webserver = models.CharField(max_length=100, blank=True, null=True, choices=WEBSERVER_CHOICES)
    deployment_database = models.CharField(max_length=100, blank=True, null=True, choices=DATABASE_CHOICES)
    deployment_method = models.CharField(max_length=100, blank=True, null=True, choices=METHOD_CHOICES)
    deployment_django = models.CharField(max_length=100, blank=True, null=True, choices=DJANGO_CHOICES)
    deployment_python = models.CharField(max_length=100, blank=True, null=True, choices=PYTHON_CHOICES)

    language = models.CharField('Content Language', max_length=10, blank=True, null=True, choices=LANGUAGE_CHOICES)

    redo_screenshot = models.BooleanField('Re-Take Screenshot?', blank=True, default=False, help_text='Do you want us to take another screenshot?')

    twitter_notified = models.BooleanField('Twitter Updated?', blank=True, default=False, editable=False)

    alexa_rank = models.IntegerField(blank=True, null=True, editable=False)

    def get_absolute_url(self):
        return '/s/%s/' % self.slug

    def __str__(self):
        return self.url
    
    def get_score(self):
        return Vote.objects.get_score(self)['score']
    
    def get_num_votes(self):
        return Vote.objects.get_score(self)['num_votes']
    
    def screenshot_uri(self):
        return '/var/python-envs/djangosites/htdocs/screenshots/%s.jpg' % self.id
    
    def largescreenshot_uri(self):
        return '/var/python-envs/djangosites/htdocs/screenshots-large/%s.jpg' % self.id
    
    def screenshot_url(self):
        return 'http://www.djangosites.org/media/screenshots/%s.jpg' % self.id
    
    def largescreenshot_url(self):
        return 'http://www.djangosites.org/media/screenshots-large/%s.jpg' % self.id
    
    def save(self, force_insert=False, force_update=False):
        if not self.owner:
            self.owner = threadlocals.get_current_user()


        if not self.redo_screenshot:
            self.redo_screenshot = False
        
        if not self.id:
            self.created = datetime.now()
            self.votes = 0
            self.num_votes = 0
            self.screenshot = 'none'
            self.verified = False
        else:
            self.votes = self.get_score()
            self.num_votes = self.get_num_votes()

        self.slug = self.url.replace("http://", "").replace("https://", "").replace("/", "-").replace(".", "-").lower()
        if self.slug[-1] == '-':
            self.slug = self.slug[:-1]
       
        try:
            colon_pos = self.slug.index(":")
        except ValueError:
            colon_pos = -1
        if colon_pos != -1:
            self.slug = self.slug[:colon_pos]
        
        #if len(self.slug)>50:
            #self.slug = self.slug[-50:]
        
        super(Website, self).save(force_insert, force_update)
    
    models.signals.post_save.connect(update_website_votes, sender=Vote)


class DeploymentStat(models.Model):
    """
    A snapshot of the Django Deployment stats at a particular point in time.
    """
    date = models.DateField()
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=200)
    count = models.DecimalField(decimal_places=1, max_digits=5) # Percentage

    def __unicode__(self):
        return '%s %s' % (self.date, self.type)

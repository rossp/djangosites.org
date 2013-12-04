#!/usr/bin/python
import time
from django.core.management import setup_environ
import settings
setup_environ(settings)

from djangosites.websites.models import Website
from django.db.models import Q

import hashlib

from urllib import urlencode
from datetime import datetime

import os

failure = []

sites = Website.objects.filter(Q(screenshot='none') | Q(redo_screenshot=True))
for site in sites:
    #site.screenshot = 'updating'
    #site.save()
    
    date = datetime.utcnow().strftime("%Y%m%d")
    m = hashlib.md5()
    m.update('%s%s%s' % (date, site.url, settings.WEBTHUMB_API_KEY))
    hash = m.hexdigest()

    params = urlencode({
        'user': 325,
        'url': site.url,
        'hash': hash,
        'size': 'medium2',
        'cache': -1,
    })

    url = "http://webthumb.bluga.net/easythumb.php?%s" % params
    
    os.system('wget -q "%s" -O %s' % (url, site.screenshot_uri()))

    attempt = 1
    while os.path.getsize(site.screenshot_uri()) < 400 and attempt < 3:
        time.sleep(7)
        os.system('wget -q "%s" -O %s' % (url, site.screenshot_uri()))
        attempt += 1

    params = urlencode({
        'user': 325,
        'url': site.url,
        'hash': hash,
        'size': 'large',
        'cache': -1,
    })

    url = "http://webthumb.bluga.net/easythumb.php?%s" % params
    
    os.system('wget -q "%s" -O %s' % (url, site.largescreenshot_uri()))

    attempt = 1
    while os.path.getsize(site.largescreenshot_uri()) < 400 and attempt < 3:
        time.sleep(7)
        os.system('wget -q "%s" -O %s' % (url, site.largescreenshot_uri()))
        attempt += 1

    if os.path.getsize(site.screenshot_uri()) < 600 and attempt >= 3:
        failure.append('%s: %s' % (site.id, site.url))
    else:
        site.screenshot = 'ok'
        site.redo_screenshot = False
        site.save()

if len(failure) > 0:
    print "Failures on: "
    print ", ".join(failure)

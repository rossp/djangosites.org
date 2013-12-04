#!/usr/bin/python
from django.core.management import setup_environ
import settings
setup_environ(settings)

from djangosites.websites.models import Website

from websites.get_alexa_rank import get_alexa_rank

for site in Website.objects.all():
    print site.url
    result = get_alexa_rank(site.url)

    if result[1] > 0:
        site.alexa_ranking = result[1]
    else:
        site.alexa_ranking = None
    site.save()
    print site.alexa_ranking

from djangosites.websites.models import Website
from tagging.models import Tag
from django.core.cache import cache

def tagcloud(request):
    cache_key = 'djangosites_sidebar_tag_cloud'
    cache_timeout = 120
    cloud = cache.get(cache_key, None)
    if not cloud:
        cloud = Tag.objects.cloud_for_model(Website, min_count=10, filters={'verified': 'True',}, steps=8)
        cache.set(cache_key, cloud, cache_timeout)
    return {'tagcloud': cloud,}

from django.contrib.syndication.views import Feed
from tagging.utils import get_tag
from djangosites.websites.models import Website
from tagging.models import Tag, TaggedItem
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class LatestSitesFeed(Feed):
    title = "djangosites.org"
    link = "/"
    description = "A listing of the latest additions to www.djangosites.org - the most comprehensive directory of websites powered by Django."

    def items(self):
        return Website.objects.filter(verified=True).order_by('-created')[:10]

    def item_pubdate(self, item):
        return item.created

    def item_author_name(self, item):
        return item.owner.username

    def item_author_link(self, item):
        return 'http://www.djangosites.org/author/%s/' % item.owner.username

    def item_enclosure_url(self, item):
        return item.screenshot_url()

    def item_enclosure_length(self, item):
        import os
        stats = os.stat(item.screenshot_uri())
        return stats.st_size

    item_enclosure_mime_type = 'image/jpeg'

class SitesByTagFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 2:
            raise ObjectDoesNotExist
        obj = Tag.objects.get(name__exact=bits[0])
        tag_instance = get_tag(obj.name)
        if tag_instance is None:
            raise Http404, 'No Tag found matching "%s"' % tag
        return tag_instance
    
    def title(self, obj):
        return "djangosites.org: Sites tagged with [%s]" % obj.name

    def description(self, obj):
        return "Additions to www.djangosites.org tagged with [%s]" % obj.name
    
    def link(self, obj):
        return "/tag/%s/" % obj.name

    def items(self, obj):
        return TaggedItem.objects.get_by_model(Website, obj).filter(verified=True).order_by('-created')[:10]

    def item_author_name(self, item):
        return item.owner.username

    def item_author_link(self, item):
        return 'http://www.djangosites.org/author/%s/' % item.owner.username

    def item_enclosure_url(self, item):
        return item.screenshot_url()

    def item_enclosure_length(self, item):
        import os
        stats = os.stat(item.screenshot_uri())
        return stats.st_size

    item_enclosure_mime_type = 'image/jpeg'

    def item_pubdate(self, item):
        return item.created


class SitesByAuthorFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 2:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])
    
    def title(self, obj):
        return "djangosites.org: Sites submitted by %s" % obj.username

    def description(self, obj):
        return "Additions to www.djangosites.org by %s" % obj.username
    
    def link(self, obj):
        return "/author/%s/" % obj.username

    def items(self, obj):
        return Website.objects.filter(verified=True).filter(owner=obj).order_by('-created')[:10]

    def item_author_name(self, item):
        return item.owner.username

    def item_author_link(self, item):
        return 'http://www.djangosites.org/author/%s/' % item.owner.username

    def item_enclosure_url(self, item):
        return item.screenshot_url()

    def item_enclosure_length(self, item):
        import os
        stats = os.stat(item.screenshot_uri())
        return stats.st_size

    item_enclosure_mime_type = 'image/jpeg'

    def item_pubdate(self, item):
        return item.created

class AllSitesByTagFeed(SitesByTagFeed):
    """
        Show all sites for a tag rather than just 10.
    """
    
    def title(self, obj):
        return "djangosites.org: All Sites tagged with [%s]" % obj.name

    def description(self, obj):
        return "All sites listed on www.djangosites.org tagged with [%s]" % obj.name
    
    def items(self, obj):
        return TaggedItem.objects.get_by_model(Website, obj).filter(verified=True).order_by('-created')

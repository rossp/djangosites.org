from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from djangosites.websites.models import Website
from voting.views import vote_on_object
from tagging.views import tagged_object_list
from djangosites.websites.feeds import LatestSitesFeed, SitesByAuthorFeed, SitesByTagFeed, AllSitesByTagFeed

from django.contrib import admin
admin.autodiscover()

tag_dict = {
    'queryset_or_model': Website.objects.filter(verified=True).select_related(),
    'paginate_by': 12,
    'allow_empty': True,
    'template_object_name': 'website',
    'template_name': 'websites/website_list.html',
    'extra_context': {'page_title': 'Items by Tag', 'view': 'tag'},
}

urlpatterns = patterns('',
    (r'^$',                 'djangosites.websites.views.latest'),
    (r'^latest/$',          RedirectView.as_view(url='/', permanent=True)),
    (r'^highest-rated/$',   'djangosites.websites.views.by_rating'),
    (r'^with-source/$',     'djangosites.websites.views.with_source'),
    (r'^upcoming/$',        'djangosites.websites.views.upcoming'),

    (r'^author/unclaimed/$',        RedirectView.as_view(url='/unclaimed/', permanent=True)),
    (r'^unclaimed/$',       'djangosites.websites.views.unclaimed'),
    
    (r'^rss/latest/$', LatestSitesFeed()),
    (r'^rss/author/$', SitesByAuthorFeed()),
    (r'^rss/tag/$', SitesByTagFeed()),
    (r'^rss/tag_full/$', AllSitesByTagFeed()),

    url(r'^accounts/$', login_required(TemplateView.as_view(template_name='account_settings.html')), name='statusping'),

    (r'^accounts/', include('django_authopenid.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^submit/$',          'djangosites.websites.views.submit'),

    (r'^tag/(?P<tag>[^/]+(?u))/$',    tagged_object_list, dict(tag_dict)),
    (r'^tags/$', 'djangosites.websites.views.tag_cloud'),
    
    (r'^author/(?P<username>[A-Za-z0-9-_+@.]+)/$',        'djangosites.websites.views.sites_by_author'),
    
    (r'^search/$',                    'djangosites.websites.views.search'),
    
    (r'^stats/$',                    'djangosites.websites.views.deployment_stats'),

    (r'^s/(?P<slug>[A-Za-z0-9-_+]+)/$',        'djangosites.websites.views.website_detail'),
    (r'^s/(?P<slug>[A-Za-z0-9-_+]+)/edit/$',    'djangosites.websites.views.update_website'),
    (r'^s/(?P<slug>[A-Za-z0-9-_+]+)/(?P<direction>up|down|clear)vote/?$',
        vote_on_object, dict(model=Website, template_object_name='website',
        template_name='website_confirm_vote.html', 
        allow_xmlhttprequest=True,
        slug_field='slug')),
    
    (r'^sitemap.xml$', TemplateView.as_view(template_name='sitemap.xml')),
    
    url(r'^statusping/$', TemplateView.as_view(template_name='statusping.html'), name='statusping'),

    url(r'^flag/$', include('flag.urls')),

)

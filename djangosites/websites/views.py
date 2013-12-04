from django.contrib.auth.models import User
from django.shortcuts import Http404, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from djangosites.websites.models import Website
from djangosites.websites.forms import WebsiteForm
from tagging.models import Tag
from tagging.utils import calculate_cloud, LOGARITHMIC
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q

def website_detail(request, slug):
    w = get_object_or_404(Website, slug=slug)

    if w.tags:
        try:
            related_tags = Tag.objects.related_for_model(w.tags, Website, counts=True)
            tag_cloud = calculate_cloud(related_tags)
        except:
            tag_cloud = []
    else:
        tag_cloud = []

    return render_to_response('websites/website_detail.html', RequestContext(request, {
        'object': w,
        'related_tag_cloud': tag_cloud,
        }))

def sites_by_author(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    
    websites = Website.objects.filter(verified=True).filter(owner=user).order_by('-created',).select_related()
    
    return render_to_response('websites/website_list.html', RequestContext(request, {
        'website_list': websites,
        'page_title': 'Sites by Owner: %s' % username,
        'view': 'author',
        'author': user,
        }))

@login_required
def update_website(request, slug):
    website = get_object_or_404(Website, slug=slug)
    
    if website.owner != request.user:
        raise Http404

    if request.method == 'POST':
        form = WebsiteForm(request.POST, instance=website)
        if form.is_valid():
            website = form.save()
            return HttpResponseRedirect(website.get_absolute_url())
    else:
        form = WebsiteForm(instance=website)

    return render_to_response('websites/website_form.html', RequestContext(request, {
        'page_title': 'Edit Your Site',
        'editing': True,
        'form': form,
        }))


def tag_cloud(request):
    cloud = Tag.objects.cloud_for_model(Website, steps=8, distribution=LOGARITHMIC, filters={'verified': 'True',})
    return render_to_response('tag_cloud.html', {
        'cloud': cloud,
        'view': 'tags',
        'page_title': 'All Tags',
    })

def search(request):
    query = request.GET.get('query', False)

    if query:
        keywords = "|".join(query.split())
        websites = Website.objects.select_related().extra(
            select={
                #'rank': "rank(search_tsv, %s)",
                'rank': "ts_rank_cd(search_tsv, plainto_tsquery(%s), 32)",
                },
            where=["search_tsv @@ plainto_tsquery(%s)"],
            params=[keywords],
            select_params=[keywords],
            order_by=('-rank',),
            )
        
        return render_to_response('websites/website_list.html', RequestContext(request, {
            'website_list': websites,
            'page_title': 'Search For Term: %s' % query,
            'view': 'search',
            'query': query,
            }))
    else:
        return render_to_response('search.html', {
            'view': 'search',
            'page_title': 'Keyword Search',
        })
    
def deployment_stats(request):
    from django.db import connection

    stats = []

    cursor = connection.cursor()
    cursor.execute("""
        SELECT      deployment_database as type,
                    COUNT(*) AS count
            FROM    websites_website w
            WHERE   deployment_database <> ''
                AND verified='t'
            GROUP BY deployment_database
            ORDER BY count DESC
    """)

    db_data = cursor.fetchall()
    data = []
    total_value = 0
    
    for row in db_data:
        total_value += row[1]
    
    for row in db_data:
        value = row[1]/float(total_value)*100
        data.append({'type': row[0], 'count': "%.1f" % value})
        
    stats.append({'title': 'Database Back-End', 'data': data})



    cursor.execute("""
        SELECT      deployment_webserver as type,
                    COUNT(*) AS count
            FROM    websites_website w
            WHERE   deployment_webserver <> ''
                AND verified='t'
            GROUP BY deployment_webserver
            ORDER BY count DESC
    """)

    db_data = cursor.fetchall()
    data = []
    total_value = 0
    
    for row in db_data:
        total_value += row[1]
    
    for row in db_data:
        value = row[1]/float(total_value)*100
        data.append({'type': row[0], 'count': "%.1f" % value})
        
    stats.append({'title': 'Webserver', 'data': data})

    cursor.execute("""
        SELECT      deployment_method as type,
                    COUNT(*) AS count
            FROM    websites_website w
            WHERE   deployment_method <> ''
                AND verified='t'
            GROUP BY deployment_method
            ORDER BY count DESC
    """)

    db_data = cursor.fetchall()
    data = []
    total_value = 0
    
    for row in db_data:
        total_value += row[1]
    
    for row in db_data:
        value = row[1]/float(total_value)*100
        data.append({'type': row[0], 'count': "%.1f" % value})
        
    stats.append({'title': 'Serving Method', 'data': data})

    cursor.execute("""
        SELECT      deployment_os as type,
                    COUNT(*) AS count
            FROM    websites_website w
            WHERE   deployment_os <> ''
                AND verified='t'
            GROUP BY deployment_os
            ORDER BY count DESC
    """)

    db_data = cursor.fetchall()
    data = []
    total_value = 0
    
    for row in db_data:
        total_value += row[1]
    
    for row in db_data:
        value = row[1]/float(total_value)*100
        data.append({'type': row[0], 'count': "%.1f" % value})
        
    stats.append({'title': 'Operating System', 'data': data})
    
    cursor.execute("""
        SELECT      deployment_django as type,
                    COUNT(*) AS count
            FROM    websites_website w
            WHERE   deployment_django <> ''
                AND verified='t'
            GROUP BY deployment_django
            ORDER BY deployment_django, count
    """)

    db_data = cursor.fetchall()
    data = []
    total_value = 0
    
    for row in db_data:
        total_value += row[1]
    
    for row in db_data:
        value = row[1]/float(total_value)*100
        data.append({'type': row[0], 'count': "%.1f" % value})
        
    stats.append({'title': 'Django Release', 'data': data})
    
    cursor.execute("""
        SELECT      deployment_python as type,
                    COUNT(*) AS count
            FROM    websites_website w
            WHERE   deployment_python <> ''
                AND verified='t'
            GROUP BY deployment_python
            ORDER BY deployment_python, count
    """)

    db_data = cursor.fetchall()
    data = []
    total_value = 0
    
    for row in db_data:
        total_value += row[1]
    
    for row in db_data:
        value = row[1]/float(total_value)*100
        data.append({'type': row[0], 'count': "%.1f" % value})
        
    stats.append({'title': 'Python Version', 'data': data})

    num_responses = Website.objects.filter(verified=True).filter(Q(deployment_database__isnull=False) | Q(deployment_webserver__isnull=False) | Q(deployment_method__isnull=False) | Q(deployment_os__isnull=False) | Q(deployment_django__isnull=False) | Q(deployment_python__isnull=False)).count()
    
    return render_to_response('deployment_stats.html', RequestContext(request, {
        'stats': stats,
        'num_sites': Website.objects.filter(verified=True).count(),
        'num_responses': num_responses,
    }))

    

def latest(request):
    websites = Website.objects.filter(verified=True).order_by('-created',).select_related()

    return render_to_response('websites/website_list.html', RequestContext(request, {
        'website_list': websites,
        'page_title': 'Latest Additions',
        'view': 'latest',
        'hits': websites.count(),
        }))

def by_rating(request):
    websites = Website.objects.filter(verified=True,num_votes__gt=0).order_by('-votes', '-num_votes',).select_related()[:10]

    return render_to_response('websites/website_topmost.html', RequestContext(request, {
        'website_list': websites,
        'page_title': 'Highest Rated Websites',
        }))

def by_comments(request):
    websites = Website.objects.filter(verified=True, comment_count__gt=0).order_by('-comment_count',).select_related()
    
    return render_to_response('websites/website_list.html', RequestContext(request, {
        'website_list': websites,
        'page_title': 'Most Commented',
        'view': 'most_commented',
        }))

def with_source(request):
    websites = Website.objects.filter(verified=True).exclude(source_url='').exclude(source_url__isnull=True).order_by('-created',).select_related()
    
    return render_to_response('websites/website_list.html', RequestContext(request, {
        'website_list': websites,
        'page_title': 'Sites with Source Code',
        'view': 'with_source',
        }))
    
def upcoming(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    
    websites = Website.objects.filter(verified=False).order_by('-created').select_related()
    
    return render_to_response('websites/website_list.html', RequestContext(request, {
        'website_list': websites,
        'page_title': 'Unapproved Websites',
        'warning': '1',
        }))

def unclaimed(request):
    websites = Website.objects.filter(verified=True, owner__username='unclaimed').order_by('title').select_related()
    
    return render_to_response('websites/website_list.html', RequestContext(request, {
        'website_list': websites,
        'page_title': 'Unclaimed Websites',
        'warning': '1',
        'view': 'unclaimed',
        }))

@login_required
def submit(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            website = form.save(commit=False)
            website.owner = request.user
            website.save()
            return HttpResponseRedirect('/submit/done/')
    else:
        form = WebsiteForm()
    
    return render_to_response('websites/website_form.html', RequestContext(request, {
        'page_title': 'Submit A Site',
        'editing': False,
        'form': form,
    }))

def sites_by_language(request, language):
    from websites.models import LANGUAGE_CHOICES
    if language not in LANGUAGE_CHOICES.keys():
        raise Http404
    
    websites = Website.objects.filter(verified=True).filter(owner=user).order_by('-created',).select_related()
    
    return render_to_response('websites/website_list.html', RequestContext(request, {
        'website_list': websites,
        'page_title': 'Sites by Owner: %s' % username,
        'view': 'author',
        'author': user,
        }))


from django.contrib import admin
from djangosites.websites.models import Website
from django.conf import settings
from django.core.mail import send_mail


class WebsiteAdmin(admin.ModelAdmin):
    list_filter = ('verified', 'screenshot',)
    list_display = ('url', 'title', 'owner', 'created', 'verified', )
    search_fields = ('title',)
    actions = ['make_verified', 'make_verified_silent', 'retake_screenshot']
    
    def retake_screenshot(self, request, queryset):
        queryset.update(redo_screenshot=True)
        num = queryset.count()
        self.message_user(request, 'Asked for %s new screenshots' % num)
    retake_screenshot.short_description = "Re-take screenshots"

    def make_verified(self, request, queryset, send_twitter=True):
        item_count = 0
        import twitter, bitly
        import tweepy
        twitter_api = None
        if send_twitter:
            twitter_auth = tweepy.OAuthHandler(settings.TWITTER_OAUTH_CONSUMER_KEY, settings.TWITTER_OAUTH_CONSUMER_SECRET)
            twitter_auth.set_access_token(settings.TWITTER_OAUTH_ACCESS_KEY, settings.TWITTER_OAUTH_ACCESS_SECRET)
            twitter_api = tweepy.API(twitter_auth)

        for item in queryset:
            item_count += 1
            item.verified = True
            posted_twitter = False

            if send_twitter and not item.twitter_notified:
                url_api = bitly.Api(login=settings.BITLY_USERNAME, apikey=settings.BITLY_APYKEY)
                short_url = url_api.shorten("http://www.djangosites.org%s" % item.get_absolute_url())

                total_length_left = 140 - len(short_url) - len(item.owner.username) - len("Just listed '' by ; ") - 1
                truncated_title = item.title[:total_length_left]
                #try:
                status = twitter_api.update_status("Just listed '%s' by %s; %s" % (truncated_title, item.owner, short_url))
                    #status = api.PostUpdate("Just listed '%s' by %s; %s" % (truncated_title, item.owner, short_url))
                #except:
                    #pass
                    # dodgy to prevent this completely dying on us
                item.twitter_notified = True
                posted_twitter = True
            item.save()

            if posted_twitter:
                twitter_text = "- a tweet linking to this listing was also posted over at https://twitter.com/djangosites."
            else:
                twitter_text = ""

            message = """Hi!

I've just checked the listing you submitted to www.djangosites.org and it checks out OK - it looks like you really do use Django. As such, I've published your listing which can now be seen at http://www.djangosites.org%s %s

Let me know if I can help at all - just respond to this e-mail.

Cheers,

Ross Poulton
Curator, Djangosites.org
""" % (item.get_absolute_url(), twitter_text)

            send_mail('Your djangosites.org listing is live', message, 'DjangoSites <djangosites@djangosites.org>', [item.owner.email])
        
        if item_count == 1:
            count_bit = "1 website was"
        else:
            count_bit = "%s websites were" % item_count

        msg = '%s successfully marked as verified' % count_bit
        if send_twitter:
            msg = msg + ' and Twitter updated'
        self.message_user(request, msg)
    make_verified.short_description = "Mark as Verified"
    
    def make_verified_silent(self, request, queryset):
        return self.make_verified(request, queryset, send_twitter=False)
    make_verified_silent.short_description = "Mark as Verified (No Twitter)"
    

admin.site.register(Website, WebsiteAdmin)

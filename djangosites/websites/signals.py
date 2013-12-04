def update_website_votes(sender, instance, signal, **kwargs):
    """
    When a Vote is added, re-saves the website to update it's count. Since Votes can be assigned
    to any content type, first makes sure we are dealing with a website.
    """
    from djangosites.websites.models import Website
    vote = instance
    if vote.content_type.name == "website":
        website=Website.objects.get(id=vote.object.id)
        website.save()

def update_website_comment_count(sender, instance, signal, **kwargs):
    """
    When a Comment is added, re-saves the website to update it's count. Since Comments can be assigned
    to any content type, first makes sure we are dealing with a website.
    """
    from djangosites.websites.models import Website
    comment = instance
    if comment.content_type.name == "website":
        website=Website.objects.get(id=comment.object_pk)
        website.save()
            

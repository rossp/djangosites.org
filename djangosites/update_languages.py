from tagging.models import Tag
from websites.models import LANGUAGE_CHOICES

#LANGUAGE_CHOICES=(('zh', 'Chinese'))

for language in LANGUAGE_CHOICES:
    code = language[0]
    name = language[1]
    print '%s: %s' % (code, name)

    try:
        tag = Tag.objects.get(name__iexact=name)
    except:
        tag = None

    if tag:
        print '     Tag: %s' % tag
        for item in tag.items.all():
            print '          Website: %s' % item.object
            if item.object:
                website = item.object
                website.language=code
                website.tags.remove(tag)
                website.save()

            #item.delete()

        #tag.delete()

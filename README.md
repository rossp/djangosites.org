## Djangosites.org Source Code

This repository holds source code used to run www.djangosites.org.

I do NOT suggest you use this, however some parts might be useful for reference (such as search indexing, thumbnail generation, etc).

The design is NOT open source and can not be used.

The Python code comes with no warranties and may be used under the terms of an MIT licence, however I don't reccommend it. There's not really any best practices in here, and it's a codebase that was written many releases of Django ago and has been upgraded ad-hoc since then. 

I'm publishing this due to many requests - and in reality, the code for such a project should be visible if it's to be a credible part of the Django community. That said, I am not actively looking for changes or improvements, however suggestions are welcome.

All content on djangosites.org is covered by the copyright notice on the page; the website content isn't included in this repository.

## What's Included

1. Signup and login with OpenID
2. Site submission by authenticated users; submitted sites are held for admin approval
3. Admin approval posts to Twitter
4. Outgoing emails sent via Mandrill using djrill
5. Website screenshots taken with http://webthumb.bluga.net

## What's Missing

This code will *not* run as-is as it's taken from a production website with very specific configs.

1. You will need to create a local_settings.py file. See the example included.
2. Setup a crontab to run get_thumbs.py
3. Configure [full-text indexing in PostgreSQL](http://www.rossp.org/blog/2009/jan/28/django-postgresql-fulltext) for search
4. Signup for Twitter, Mandrill, Bitly, Webthumb to get API keys.
5. You must write your own templates; included .html files are for example purposes only
6. No deployment files are included (ie wsgi or similar config)
7. Tests. This is a simple site that's been running for a relatively long time. It isn't under active development. If active development were to begin, tests would be critical.
8. Support of any time. I can try to answer questions but I don't intend to support usage of this package as-is.

###

Happy coding!

Ross Poulton, December 2013
ross@rossp.org
http://www.rossp.org

#!/usr/bin/env python
import sys
import re
import urllib2

def get_alexa_rank(url):
    try:
        data = urllib2.urlopen('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (url)).read()

        reach_rank = re.findall("REACH[^\d]*(\d+)", data)
        if reach_rank: reach_rank = reach_rank[0]
        else: reach_rank = -1

        popularity_rank = re.findall("POPULARITY[^\d]*(\d+)", data)
        if popularity_rank: popularity_rank = popularity_rank[0]
        else: popularity_rank = -1

        return int(popularity_rank), int(reach_rank)

    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return None
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python %s <site-url>' % (sys.argv[0])
        sys.exit(2)

    url = sys.argv[1]
    data = get_alexa_rank(url)

    popularity_rank, reach_rank = -1, -1
    if data:
        popularity_rank, reach_rank = data

    print 'popularity rank = %d\nreach_rank = %d' % (popularity_rank, reach_rank)

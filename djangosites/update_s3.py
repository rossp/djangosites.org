"""
Takes a list of filenames via standard input and uploads them to Amazon S3.

Requires S3.py:
    http://developer.amazonwebservices.com/connect/entry.jspa?externalID=134&categoryID=47

Usage:
    cd /directory/with/media/files/
    find | grep -v ".svn" | python /path/to/update_s3.py

Before you use this, change the AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and
BUCKET_NAME variables at the top of the file.

You can run this multiple times on the same files -- it'll just override the
files that were in your S3 account previously.
"""

import mimetypes
import os.path
import sys
import S3 # Get this from Amazon
import settings


def update_s3():
    conn = S3.AWSAuthConnection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    for line in sys.stdin:
        filename = os.path.normpath(line[:-1])
        if filename == '.' or not os.path.isfile(filename):
            continue # Skip this, because it's not a file.
        print "Uploading %s" % filename
        filedata = open(filename, 'rb').read()
        content_type = mimetypes.guess_type(filename)[0]
        if not content_type:
            content_type = 'text/plain'
        conn.put(settings.BUCKET_NAME, filename, S3.S3Object(filedata),
            {'x-amz-acl': 'public-read', 'Content-Type': content_type})

if __name__ == "__main__":
    update_s3()

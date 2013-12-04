#!/usr/bin/python
    
from django.core.management import setup_environ
import settings
setup_environ(settings)


from djangosites.websites.models import Website, DeploymentStat
from django.db import connection
from datetime import date

cursor = connection.cursor()

today = date.today()
stats = []

cursor.execute("""
    SELECT      deployment_database as type,
                COUNT(*) AS count
        FROM    websites_website w
        WHERE   deployment_database <> ''
            AND verified='t'
        GROUP BY deployment_database
        ORDER BY deployment_database, count
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
        ORDER BY deployment_webserver, count
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
        ORDER BY deployment_method, count
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
        ORDER BY deployment_os, count
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

for item in stats:
    for value in item['data']:
        s = DeploymentStat(
            date=today,
            type = item['title'],
            value = value['type'],
            count = value['count'],
            )
        s.save()

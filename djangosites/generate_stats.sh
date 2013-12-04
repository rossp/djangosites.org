:
#export PYTHONPATH=/var/django
#export DJANGO_SETTINGS_MODULE=djangosites.settings
cd /var/python-envs/djangosites/djangosites
. ../bin/activate
python generate_stats.py

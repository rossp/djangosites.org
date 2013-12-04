
from south.db import db
from django.db import models
from djangosites.websites.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Website'
        db.create_table('websites_website', (
            ('id', orm['websites.Website:id']),
            ('title', orm['websites.Website:title']),
            ('url', orm['websites.Website:url']),
            ('slug', orm['websites.Website:slug']),
            ('owner', orm['websites.Website:owner']),
            ('description', orm['websites.Website:description']),
            ('tags', orm['websites.Website:tags']),
            ('verified', orm['websites.Website:verified']),
            ('created', orm['websites.Website:created']),
            ('comment_count', orm['websites.Website:comment_count']),
            ('num_votes', orm['websites.Website:num_votes']),
            ('votes', orm['websites.Website:votes']),
            ('screenshot', orm['websites.Website:screenshot']),
            ('webthumb_key', orm['websites.Website:webthumb_key']),
            ('source_url', orm['websites.Website:source_url']),
            ('sotw_url', orm['websites.Website:sotw_url']),
            ('deployment_os', orm['websites.Website:deployment_os']),
            ('deployment_webserver', orm['websites.Website:deployment_webserver']),
            ('deployment_database', orm['websites.Website:deployment_database']),
            ('deployment_method', orm['websites.Website:deployment_method']),
            ('deployment_django', orm['websites.Website:deployment_django']),
            ('deployment_python', orm['websites.Website:deployment_python']),
            ('redo_screenshot', orm['websites.Website:redo_screenshot']),
        ))
        db.send_create_signal('websites', ['Website'])
        
        # Adding model 'DeploymentStat'
        db.create_table('websites_deploymentstat', (
            ('id', orm['websites.DeploymentStat:id']),
            ('date', orm['websites.DeploymentStat:date']),
            ('type', orm['websites.DeploymentStat:type']),
            ('value', orm['websites.DeploymentStat:value']),
            ('count', orm['websites.DeploymentStat:count']),
        ))
        db.send_create_signal('websites', ['DeploymentStat'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Website'
        db.delete_table('websites_website')
        
        # Deleting model 'DeploymentStat'
        db.delete_table('websites_deploymentstat')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'websites.deploymentstat': {
            'count': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'websites.website': {
            'comment_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deployment_database': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'deployment_django': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'deployment_method': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'deployment_os': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'deployment_python': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'deployment_webserver': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_votes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'redo_screenshot': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'screenshot': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sotw_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'webthumb_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['websites']

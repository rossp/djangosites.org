from django import forms
from djangosites.websites.models import Website

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website

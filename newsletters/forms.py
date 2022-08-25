from django import forms

from .models import NewsletterUsers


class NewsletterUserForm(forms.ModelForm):
    
    class Meta:
        model = NewsletterUsers
        fields = ['email']

from django import forms
from .models import NewsletterUsers, MailMessage


class NewsletterUserForm(forms.ModelForm):
    class Meta:
        model = NewsletterUsers
        fields = ['email']
    

class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = ('__all__')


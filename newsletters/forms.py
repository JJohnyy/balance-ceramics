from django import forms
from .models import NewsletterUsers, MailMessage, Newsletter



class NewsletterUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
    class Meta:
        model = NewsletterUsers
        fields = ['email']
    

class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = ('__all__')


class NewsletterCreationForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'body', 'email', 'status']




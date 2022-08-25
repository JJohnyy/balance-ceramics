from django import forms

from .models import NewsletterUsers


class NewsletterUserForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False
    
    class Meta:
        model = NewsletterUsers
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

from django import forms

from .models import NewsletterUsers


class NewsletterUserForm(forms.ModelForm):
    class Meta:
        model = NewsletterUsers
        fields = ['email']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if email:
                return email
            else:
                raise forms.ValidationError("Email address is required.")

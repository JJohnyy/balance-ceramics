from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """ UserProfile form """
    class Meta:
        """ UserProfile form """
        model = UserProfile
        fields = (
            'default_phone_number',
        )
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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
        }

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            self.fields[field].widget.attrs.update({
                'placeholder': placeholder,
            })
        self.fields['default_phone_number'].label = 'Phone number'


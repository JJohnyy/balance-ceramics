from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """ UserProfile form """
    class Meta:
        """ UserProfile form """
        model = UserProfile
        fields = (
            'default_phone_number',
            'default_postcode',
            'default_town_or_city',
            'default_street_address1',
            'default_street_address2',
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
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


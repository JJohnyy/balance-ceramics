from django import forms
from .models import Mugs, MugsCategory


class ProductForm(forms.ProductForm):
    
    class Meta:
        model = Mugs
        fields = '__all__'

    image = models.ImageField(label='Image', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = MugsCategory.object.all()
        friendly_names = [c.id, c.get_friendly_name() for c in categories]
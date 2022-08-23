from django.contrib import admin
from . models import Mugs, MugsCategory

# Register your models here.

class MugsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'category',
        'price',
        'image',
        'slug_name'
        )


class MugsCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
    )

admin.site.register(Mugs, MugsAdmin)
admin.site.register(MugsCategory, MugsCategoryAdmin)

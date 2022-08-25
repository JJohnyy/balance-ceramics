from django.contrib import admin
from .models import NewsletterUsers, MailMessage


# Register your models here.

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_added',)

class MailMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'message',)


admin.site.register(NewsletterUsers, NewsletterAdmin)
admin.site.register(MailMessage, MailMessageAdmin)



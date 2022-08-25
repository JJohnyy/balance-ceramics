from django.db import models

# Create your models here.

class NewsletterUsers(models.Model):
    is_subscribed = models.BooleanField(default=False)
    email = models.EmailField(
        max_length=254,
        null=False,
        blank=False
    )
    date_added = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.email

    class Meta:
        """ change verbose name in Admin"""
        verbose_name_plural = 'Newsletter Users'

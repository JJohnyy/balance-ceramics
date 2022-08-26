from django.db import models

# Create your models here.

class NewsletterUsers(models.Model):
    email = models.EmailField(
        max_length=254,
        null=True,
        blank=True
    )
    date_added = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.email

    class Meta:
        """ change verbose name in Admin"""
        verbose_name_plural = 'Newsletter Users'


class MailMessage(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    EMAIL_STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    email = models.ManyToManyField(NewsletterUsers)
    status = models.CharField(max_length=10, choices=EMAIL_STATUS_CHOICES)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

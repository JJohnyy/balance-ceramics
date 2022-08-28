from django.db import models

# Create your models here.


class MugsCategory(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        """ change verbose name in Admin"""
        verbose_name_plural = 'MugCategories'


class Mugs(models.Model):
    category = models.ForeignKey(
        'MugsCategory',
        null=True, blank=True,
        on_delete=models.SET_NULL
        )
    name = models.CharField(max_length=254)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    slug_name = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        """ change verbose name in Admin """
        verbose_name_plural = 'Mugs'

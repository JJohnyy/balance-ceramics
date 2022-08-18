import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Dishes, Wines, Bundle
from profiles.models import UserProfile

# Create your models here.

class Order(models.Model):
    """ Model for an order """

    order_number = models.CharField(
        max_length=32,
        null=False,
        editable=False
        )
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
        )
    full_name = models.CharField(
        max_length=50,
        null=False,
        blank=False
        )
    email = models.EmailField(
        max_length=254,
        null=False,
        blank=False
        )
    phone_number = models.CharField(
        max_length=20,
        null=False,
        blank=False
        )
    date = models.DateTimeField(
        auto_now_add=True
        )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
        )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
        )
    original_bag = models.TextField(
        null=False,
        blank=False,
        default=''
        )
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default=''
        )

    def __str__(self):
        return f'{self.order_number}'

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a order item is added
        """
        self.order_total = self.orderitems.aggregate(
            Sum('orderitem_total'))['orderitem_total__sum'] or 0

        self.grand_total = self.order_total
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """ Model for individual order item """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='orderitems'
    )
    mug = models.ForeignKey(
        Mugs,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
         """
        Override the original save method to set the orderitem total
        and update the order total depending on if the.
        """
        if self.mug:
            self.order_total = self.mug.price * self.quantity
            super().save(*args, **kwargs)

        else:
            return

    def __str__(self):
        return f'{self.order}'



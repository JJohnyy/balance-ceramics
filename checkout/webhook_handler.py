import json
import time

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from products.models import Mugs
from profiles.models import UserProfile

from .models import Order, OrderItem


class StripeWebhookHandler:
    """ Handle Stripe webhooks """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = billing_details.phone
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=billing_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    original_bag=bag,
                    stripe_pid=pid,
                )

                mugs = Mugs.objects.all()
                

                mug_slug_list = []
                

                for mug in mugs:
                    mug_slug_list.append(mug.slug_name)

                for item_slug, item_data in json.loads(bag).items():
                    if item_slug in dish_slug_list:
                        dish = Dishes.objects.get(slug_name=item_slug)
                        if isinstance(item_data, int):
                            order_item = OrderItem(
                                order=order,
                                dish=dish,
                                quantity=item_data,
                            )
                            order_item.save()
                    if item_slug in wine_slug_list:
                        wine = Wines.objects.get(slug_name=item_slug)
                        if isinstance(item_data, int):
                            order_item = OrderItem(
                                order=order,
                                wine=wine,
                                quantity=item_data,
                            )
                            order_item.save()
                    if item_slug in bundle_slug_list:
                        bundle = Bundles.objects.get(slug_name=item_slug)
                        if isinstance(item_data, int):
                            order_item = OrderItem(
                                order=order,
                                bundle=bundle,
                                quantity=item_data,
                            )
                            order_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_failed(self, event):
        """
        Handle the payment intent failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order

# Create your views here.

@login_required
def profile(request):
    """
    Profile view
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Thanks {user_profile}, \
                your details have been updated.')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=user_profile)
    orders = user_profile.orders.all()

    context = {
        'form': form,
        'orders': orders,
    }

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    """ Order history """

    order = get_object_or_404(Order, order_number=order_number)

    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, 'checkout/checkout_success.html', context)

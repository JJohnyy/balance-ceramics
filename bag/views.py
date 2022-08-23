from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from products.models import Mugs

# Create your views here.

def view_bag(request):
    """ A view to return the bag page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_slug):
    """ Add a quantity of a product to the bag during a session """

    mug = get_object_or_404(Mugs, pk=item_slug)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    product_name = request.POST.get('product_name')
    bag = request.session.get('bag', {})

    if item_slug in list(bag.keys()):
        bag[item_slug] += quantity
        if quantity > 1:
            messages.success(
                request,
                f'{quantity} {product_name} mugs added to the basket'
                )
            request.session['bag'] = bag
            return redirect(redirect_url)
        else:
            messages.success(
                request,
                f'{quantity} {product_name} mugs added to the basket'
            )
            request.session['bag'] = bag
            return redirect(redirect_url)
    else:
        bag[item_slug] = quantity
    
    request.session['bag'] = bag
    return redirect(redirect_url)


def update_bag(request, item_slug):
    """ Update the quantity of a product to the bag during a session """

    if request.method == 'POST':
        quantity = int(request.POST.get('item-quantity'))
        product_name = request.POST.get('item_name')
        bag = request.session.get('bag', {})

        if item_slug in list(bag.keys()):
            if quantity > 0:
                bag[item_slug] = quantity
                messages.success(
                    request,
                    f'Quantity of {product_name.title()} successfully \
                        updated to {quantity}'
                    )
        else:
            bag[item_slug] = quantity

        request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_slug):
    """ Removes the item from the bag """

    bag = request.session.get('bag', {})
    bag.pop(item_slug)
    request.session['bag'] = bag

    messages.success(request, 'Successfully removed item from your basket')

    return redirect(reverse('view_bag'))

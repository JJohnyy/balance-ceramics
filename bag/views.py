from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from products.models import Mugs

# Create your views here.

def view_bag(request):
    """ A view to return the bag page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of a product to the bag during a session """

    mug = get_object_or_404(Mugs, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    product_name = request.POST.get('product_name')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        if quantity > 1:
            messages.success(
                request,
                f'{mug.quantity} {product_name} another mug added to the basket'
                )
    else:
        bag[item_id] = quantity
    
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def update_bag(request, item_id):
    """ Update the quantity of a product to the bag during a session """

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        product_name = request.POST.get('item_name')
        bag = request.session.get('bag', {})

        if item_id in list(bag.keys()):
            if quantity > 0:
                bag[item_id] = quantity
                messages.success(
                    request,
                    f'Quantity of {product_name} successfully \
                        updated to {quantity}'
                    )
        else:
            bag[item_id] = quantity

        request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Removes the item from the bag """
    try:
        product = get_object_or_404(Mugs, pk=item_id)

        bag = request.session.get('bag', {})
        bag.pop(item_id)
        request.session['bag'] = bag

        messages.success(request, f'Successfully removed {product.name} from basket')
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')

    return redirect(reverse('view_bag'))

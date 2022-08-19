from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import MugsCategory, Mugs
from .forms import ProductForm


# Create your views here.

def product_list(request):
    """
    view to show all products
    """
    products = Mugs.objects.all()

    sort = None
    query = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            is_sorted = True
            sortkey = request.GET['sort']
            sort = sortkey

            if sortkey == 'category__origin':
                sort = 'Origin'
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'asc':
                        direction = 'from A - Z'

            if sortkey == 'price':
                sort = 'Price'
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'asc':
                        direction = 'from low to high'
                    if direction == 'desc':
                        sortkey = f'-{sortkey}'
                        direction = 'from high to low'

            if sortkey == 'name':
                sortkey = 'lower_name'
                mugs = mugs.annotate(lower_name=Lower('name'))
                sort = 'Mug'
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'asc':
                        direction = 'from A - Z'
                    if direction == 'desc':
                        sortkey = f'-{sortkey}'
                        direction = 'from Z - A'

            mugs = mugs.order_by('sortkey')

    current_sorting = f'Search by: {sort} {direction}'

    #context = {
    #    'mugs': mugs,
     #   'current_sorting': current_sorting,
    #    'sortkey': sortkey,
    #    'query': query,
    #    'is_sorted': is_sorted,
    #}
   

    return render(request, 'products/product_list.html', {'products': products})


def product_detail_mugs(request, product_id):
    """Detailed view of a product"""
    mugs = Mugs.objects.all()
    product = get_object_or_404(Mugs, pk=product_id)

    context = {
        'product': product,
        'mugs': mugs,
    }
    return render(request, 'products/product-detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the list of products"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorrym you are not the owner')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added')
            return redirect(reverse('product-detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add the product')
    else:
        form=ProductForm()


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Mugs, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product-detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit-product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Mugs, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))







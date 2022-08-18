from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import MugsCategory, Mugs


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
   

    return render(request, 'products/product_list.html')


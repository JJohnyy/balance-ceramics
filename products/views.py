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
    return render(request, 'products/product_list.html', {'products': products})


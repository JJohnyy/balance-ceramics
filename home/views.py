from django.shortcuts import render

# Create your views here.


def index(request):
    """
    view to render index page
    """
    return render(request, 'home/index.html')


def error_404(request,exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, 'home/404.html', status=404)
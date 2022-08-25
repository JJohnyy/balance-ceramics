from django.shortcuts import render
from .models import NewsletterUsers
from .forms import NewsletterUserForm
# Create your views here.


def newsletter_signup(request):
    form = NewsletterUserForm(request.POST or None)
    
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUsers.objects.filter(user=instance.email).exists():
            print('hi')
        else:
            instance.save()

    context = {
        'form': form,
    }
    return render(request, 'newsletters/newsletters.html', context)


def newsletter_unsubscribe(request):
    form = NewsletterUserForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUsers.objects.filter(email=instance.email).exists():
            NewsletterUsers.objets.filter(email=instance.email).delete()
        else:
            print('hello')

    context = {
        'form': form,
    }
    return render(request, 'newsletters/newsletters_unsubscribe.html', context)



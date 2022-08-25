from django.shortcuts import render, redirect
from .models import NewsletterUsers, MailMessage
from .forms import NewsletterUserForm
from django.contrib import messages
# Create your views here.


def newsletter_signup(request):
    
    if request.method == 'POST':
        form = NewsletterUserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if NewsletterUsers.objects.filter(email=instance.email).exists():
                messages.error(request, 'email already exists')
            else:
                form.save()
                messages.success(request, 'Subscription Successful')
                return redirect('newsletter_signup')
    else:
        form = NewsletterUserForm()
    context = {
        'form': form,
    }
    return render(request, 'newsletters/newsletters.html', context)


def newsletter_unsubscribe(request):
    return render(request, 'newsletters/newsletters_unsubscribe.html'),




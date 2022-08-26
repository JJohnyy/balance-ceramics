from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NewsletterUsers, Newsletter
from .forms import NewsletterUserForm, NewsletterCreationForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


# Create your views here.


def newsletter_signup(request):
    
    if request.method == 'POST':
        form = NewsletterUserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if NewsletterUsers.objects.filter(email=instance.email).exists():
                messages.error(request, 'email alredy in our database')
            else:
                form.save()
                messages.error(request, 'email added successfully')
                subject = "Thank you for joining our newsletters"
                from_email = settings.EMAIL_BACKEND
                to_email = [instance.email]
                with open(str(settings.BASE_DIR) + "/newsletters/templates/newsletters/emails/sign_up_email.txt") as f:
                    signup_message = f.read()
                message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
                html_template = get_template('newsletters/sign_up_email.html').render()
                message.attach_alternative(html_template, 'text/html')
                message.send()
                

                return redirect('home')
    else:
        form = NewsletterUserForm()
    context = {
        'form': form,
    }
    return render(request, 'newsletters/newsletters.html', context)


def newsletter_unsubscribe(request):
    form = NewsletterUserForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUsers.objects.filter(email=instance.email).exists():
            NewsletterUsers.objects.filter(email=instance.email).delete()
            messages.success(request, 'email successfully deleted')
            subject = "You have been unsubscribed"
            from_email = settings.EMAIL_BACKEND
            to_email = [instance.email]
            with open(str(settings.BASE_DIR) + "/newsletters/templates/newsletters/emails/unsubscribe.txt") as f:
                    signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template('newsletters/unsubscribe.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()
            return redirect('home')
        else:
            messages.error(request, 'your email is not in our databse') 
    context = {
        'form': form,
    }
    return render(request, 'newsletters/newsletters_unsubscribe.html', context)


def control_newsletter(request):
    form = NewsletterCreationForm(request.POST)
    if form.is_valid():
        instance = form.save()
        newsletter = Newsletter.objects.get(id=instance.id)
        if newsletter.status == 'Publish':
            subject = newsletter.subject
            body = newsletter.body
            from_email = settings.EMAIL_BACKEND
            for email in newsletter.email.all():
                send_mail(subject=subject, from_email=from_email,recipient_list=[email], message=body, fail_silently=True)
                
    context = {
        'form': form,
    }

    return render(request, 'control_panel/control_newsletter.html', context)



def contact_view(request):
    return render(request, 'newsletters/contacts.html')



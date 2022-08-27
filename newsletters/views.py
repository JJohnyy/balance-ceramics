from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .models import NewsletterUsers, Newsletter
from .forms import NewsletterUserForm, NewsletterCreationForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        if newsletter.status == 'Published':
            subject = newsletter.subject
            body = newsletter.body
            from_email = settings.EMAIL_BACKEND
            for email in newsletter.email.all():
                send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)
                
    context = {
        'form': form,
    }

    return render(request, 'control_panel/control_newsletter.html', context)


def control_newsletter_list(request):
    newsletters = Newsletter.objects.all()

    paginator = Paginator(newsletters, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'items': items,
        'page_range': page_range,
    }

    return render(request, 'control_panel/control_newsletter_list.html', context)


def control_newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    context = {
        'newsletter': newsletter,
    }

    return render(request, 'control_panel/control_newsletter_detail.html', context)

  

def control_newsletter_edit(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save()
            if newsletter.status == 'Published':
                messages.success(request, 'email sent')
                subject = newsletter.subject
                body = newsletter.body
                from_email = settings.EMAIL_BACKEND
                for email in newsletter.objects.all():
                    send_mail(subject=subject, message=body, from_email=from_email, recipient_list=[email], fail_silently=True)
    else:
        form = NewsletterCreationForm(instance=newsletter)

    context = {
        'form': form,
        'newsletter': newsletter,
    }

    return redirect(request, 'control_newsletter_edit', context)



def contact_view(request):
    return render(request, 'newsletters/contacts.html')

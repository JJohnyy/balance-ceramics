from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from .models import NewsletterUsers, Newsletter
from .forms import NewsletterUserForm, NewsletterCreationForm


# Create your views here.


def newsletter_signup(request):

    if request.method == 'POST':
        form = NewsletterUserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if NewsletterUsers.objects.filter(email=instance.email).exists():
                messages.error(request, 'email alredy in our database')
                return redirect('home')
            else:
                form.save()
                messages.success(request, 'email added successfully')
                subject = "Thank you for joining our newsletters"
                from_email = settings.EMAIL_BACKEND
                to_email = [instance.email]
                with open(str
                    (settings.BASE_DIR) +
                        "/newsletters/templates/newsletters/emails/sign_up_email.txt"
                        ) as f:
                    signup_message = f.read()
                message = EmailMultiAlternatives(
                    subject=subject,
                    body=signup_message,
                    from_email=from_email,
                    to=to_email
                    )
                html_template = get_template(
                    'newsletters/sign_up_email.html').render()
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
            with open(
                     str(settings.BASE_DIR) +
                     "/newsletters/templates/newsletters/emails/unsubscribe.txt"
                     ) as f:
                signup_message = f.read()

            message = EmailMultiAlternatives(
                    subject=subject,
                    body=signup_message,
                    from_email=from_email,
                    to=to_email
                    )
            html_template = get_template(
                'newsletters/unsubscribe.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()
            return redirect('home')
        else:
            messages.error(request, 'your email is not in our databse')
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'newsletters/newsletters_unsubscribe.html', context)


# compose a new letter
@login_required
def control_newsletter(request):
    form = NewsletterCreationForm(request.POST)
    if form.is_valid():
        instance = form.save()
        newsletter = Newsletter.objects.get(id=instance.id)
        if newsletter.status == 'Published':
            messages.success(request, 'email sent')
            subject = newsletter.subject
            body = newsletter.body
            from_email = settings.DEFAULT_FROM_EMAIL
            for email in newsletter.email.all():
                send_mail(
                    subject=subject,
                    from_email=from_email,
                    recipient_list=[email],
                    message=body,
                    fail_silently=True
                    )
            return redirect('newsletter')
    context = {
        'form': form,
    }

    return render(request, 'control_panel/control_newsletter.html', context)


@login_required
def control_newsletter_list(request):
    newsletters = Newsletter.objects.all()

    paginator = Paginator(newsletters, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    number_of_pages = 'a' * items.paginator.num_pages

    context = {
        'items': items,
        'number_of_pages': number_of_pages,
    }

    return render(
        request,
        'control_panel/control_newsletter_list.html',
        context
        )


@login_required
def control_newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    context = {
        'newsletter': newsletter,
    }

    return render(request,
                  'control_panel/control_newsletter_detail.html',
                  context
                  )


@login_required
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
                from_email = settings.DEFAULT_FROM_EMAIL
                for email in newsletter.email.all():
                    send_mail(
                        subject=subject,
                        message=body,
                        from_email=from_email,
                        recipient_list=[email],
                        fail_silently=True
                        )
    else:
        form = NewsletterCreationForm(instance=newsletter)
        messages.success(request, 'email edited successfully')

    context = {
        'form': form,
        'newsletter': newsletter,
    }

    return render(request,
                  'control_panel/control_newsletter_edit.html',
                  context
                  )


@login_required
def control_newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter.delete()
            messages.success(request, 'email deleted')
            return redirect('control_newsletter_list')
    else:
        form = NewsletterCreationForm(instance=newsletter)

    context = {
        'form': form,
        'newsletter': newsletter,
    }

    return render(request,
                  'control_panel/control_newsletter_delete.html',
                  context
                  )


def contact_view(request):
    return render(request, 'newsletters/contacts.html')

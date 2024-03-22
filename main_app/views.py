from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.conf import settings
# from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'main_app/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Could add error message here...
            pass
    return render(request, 'main_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main_app/register.html', {'form': form})

def home_view(request):
    return render(request, 'main_app/home.html')

from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')

        # Creates an email message
        email_subject = 'New Contact Form Submission'
        email_body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        email = EmailMessage(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
        )

        # Attaches the file if provided
        if attachment:
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        # Sends the email
        email.send()

        # Renders a success message or redirect to a success page
        return render(request, 'main_app/contact_success.html')

    return render(request, 'main_app/contact.html')

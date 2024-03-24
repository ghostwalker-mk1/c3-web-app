from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InventoryForm
from .models import Inventory
class ChangePasswordForm(PasswordChangeForm):
    pass

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


@login_required
def my_account(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        password_form = ChangePasswordForm(request.user, request.POST)

        if 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('my_account')
        elif 'update_profile' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('my_account')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        password_form = ChangePasswordForm(request.user)

    return render(request, 'main_app/my_account.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })

def inventory_view(request):
    inventory_items = Inventory.objects.all()
    form = InventoryForm()

    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')

    return render(request, 'main_app/inventory.html', {'inventory_items': inventory_items, 'form': form})

def update_inventory(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = InventoryForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'main_app/edit_inventory.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile, Inventory, Sale, SaleItem, Claim, Product, Inspection
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InventoryForm, SaleForm, SaleItemForm, ClaimForm, UserProfileForm, InspectionForm
from django.db import models
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib, base64
import os

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

        # Renders success message
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

@login_required
def inventory_view(request):
    inventory_items = Inventory.objects.all()
    form = InventoryForm()

    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')

    return render(request, 'main_app/inventory.html', {'inventory_items': inventory_items, 'form': form})

@login_required
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

@login_required
def delete_inventory(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    item.delete()
    return redirect('inventory')

@login_required
def sales_view(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            # print(sale_form.cleaned_data)
            sale = sale_form.save()
            # print(sale)
            return redirect('add_sale_items', sale_id=sale.id)
    else:
        sale_form = SaleForm()

    sales = Sale.objects.all()
    # print(sales)
    context = {
        'sale_form': sale_form,
        'sales': sales,
    }
    # print(context)
    return render(request, 'main_app/sales_data.html', context)

@login_required
def add_sale_items(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        item_form = SaleItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.sale = sale
            item.save()
            return redirect('add_sale_items', sale_id=sale.id)
    else:
        item_form = SaleItemForm()

    items = SaleItem.objects.filter(sale=sale)
    context = {
        'sale': sale,
        'item_form': item_form,
        'items': items,
    }
    return render(request, 'main_app/add_sale_items.html', context)

@login_required
def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        sale.delete()
        return redirect('sales_data')
    context = {
        'sale': sale
    }
    return render(request, 'main_app/delete_sale.html', context)

@login_required
def claims_view(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('claims')
    else:
        form = ClaimForm()

    claims = Claim.objects.all()
    context = {
        'form': form,
        'claims': claims,
    }
    return render(request, 'main_app/claims.html', context)

@login_required
def edit_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    if request.method == 'POST':
        form = ClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            return redirect('claims')
    else:
        form = ClaimForm(instance=claim)

    context = {
        'form': form,
        'claim': claim,
    }
    return render(request, 'main_app/edit_claim.html', context)

@login_required
def delete_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    if request.method == 'POST':
        claim.delete()
        return redirect('claims')
    context = {
        'claim': claim
    }
    return render(request, 'main_app/delete_claim.html', context)

@login_required
def reporting_dashboard(request):
    # Inventory Levels Bar Chart
    inventory_data = Inventory.objects.values('name', 'quantity')
    inventory_names = [item['name'] for item in inventory_data]
    inventory_quantities = [item['quantity'] for item in inventory_data]

    fig, ax = plt.subplots()
    ax.bar(inventory_names, inventory_quantities)
    ax.set_title('')
    ax.set_xlabel('Product')
    ax.set_ylabel('Quantity')

    num_items = len(inventory_names)
    ax.set_xticks(range(0, num_items, 1))
    plt.xticks(rotation=45, ha='right')

    inventory_chart_path = os.path.join(settings.MEDIA_ROOT, 'inventory_chart.png')
    print(inventory_chart_path)
    fig.savefig(inventory_chart_path, bbox_inches='tight')

    # Claim Counts Bar Chart
    claim_data = Claim.objects.values('claim_type').annotate(count=models.Count('id'))
    claim_types = [item['claim_type'] for item in claim_data]
    claim_counts = [item['count'] for item in claim_data]

    fig, ax = plt.subplots()
    ax.bar(claim_types, claim_counts)
    ax.set_title('')
    ax.set_xlabel('Claim Type')
    ax.set_ylabel('Count')

    claim_chart_path = os.path.join(settings.MEDIA_ROOT, 'claim_chart.png')
    fig.savefig(claim_chart_path)

    # Sales Distribution by Region Pie Chart
    sales_region_data = Sale.objects.values('sales_region').annotate(count=models.Count('id'))
    region_labels = [item['sales_region'] for item in sales_region_data]
    region_counts = [item['count'] for item in sales_region_data]

    fig, ax = plt.subplots()
    ax.pie(region_counts, labels=region_labels, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('')

    sales_region_chart_path = os.path.join(settings.MEDIA_ROOT, 'sales_region_chart.png')
    fig.savefig(sales_region_chart_path)

    # Claims Distribution by Type Pie Chart
    claim_type_data = Claim.objects.values('claim_type').annotate(count=models.Count('id'))
    claim_type_labels = [item['claim_type'] for item in claim_type_data]
    claim_type_counts = [item['count'] for item in claim_type_data]

    fig, ax = plt.subplots()
    ax.pie(claim_type_counts, labels=claim_type_labels, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('')

    claim_type_chart_path = os.path.join(settings.MEDIA_ROOT, 'claim_type_chart.png')
    fig.savefig(claim_type_chart_path)

    context = {
        'inventory_chart_path': inventory_chart_path,
        'claim_chart_path': claim_chart_path,
        'sales_region_chart_path': sales_region_chart_path,
        'claim_type_chart_path': claim_type_chart_path,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'main_app/reporting_dashboard.html', context)

def get_base64_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_data = urllib.parse.quote(base64.b64encode(buf.read()))
    return image_data

def products_view(request):
    return render(request, 'main_app/products.html')

@login_required
def warranty_view(request):
    return render(request, 'main_app/warranties.html')

@login_required
def inspections_view(request):
    return render(request, 'main_app/inspections.html')

def about_us_view(request):
    return render(request, 'main_app/about_us.html')

def products_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'main_app/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'main_app/product_detail.html', context)
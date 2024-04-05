from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Inventory(models.Model):
    product_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=100)
    dealership_details = models.CharField(max_length=200)
    sales_rep_name = models.CharField(max_length=100)
    sales_rep_contact = models.CharField(max_length=100)
    sales_region = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer_name} - {self.sales_rep_name} ({self.sales_region})"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Claim(models.Model):
    claim_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    submission_date = models.DateTimeField(default=timezone.now)
    customer_name = models.CharField(max_length=100)
    dealership_details = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.claim_type} - {self.customer_name}"
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
class Inspection(models.Model):
    location = models.CharField(max_length=200)
    inspection_type = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, unique=True)
    comments = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.inspection_type} - {self.make} {self.model} ({self.vin})"
# Generated by Django 5.0.3 on 2024-04-05 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_remove_warranty_customer_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images'),
        ),
    ]
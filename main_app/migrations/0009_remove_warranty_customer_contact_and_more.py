# Generated by Django 5.0.3 on 2024-04-05 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_warranty_customer_contact_warranty_customer_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warranty',
            name='customer_contact',
        ),
        migrations.RemoveField(
            model_name='warranty',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='warranty',
            name='dealership_details',
        ),
    ]

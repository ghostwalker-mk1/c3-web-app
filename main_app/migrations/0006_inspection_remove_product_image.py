# Generated by Django 5.0.3 on 2024-04-05 18:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=200)),
                ('inspection_type', models.CharField(max_length=100)),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('vin', models.CharField(max_length=17, unique=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]

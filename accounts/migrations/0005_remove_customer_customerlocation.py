# Generated by Django 5.0.3 on 2024-05-25 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customer_customerphonenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='CustomerLocation',
        ),
    ]

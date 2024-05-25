# Generated by Django 5.0.3 on 2024-05-25 11:38

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customer_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='CustomerPhoneNumber',
            field=models.CharField(default=1, max_length=11, validators=[accounts.validators.validate_phone_number]),
            preserve_default=False,
        ),
    ]

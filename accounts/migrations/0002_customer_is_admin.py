# Generated by Django 5.0.3 on 2024-05-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_admin',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]

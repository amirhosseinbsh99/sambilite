# Generated by Django 5.0.3 on 2024-04-13 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='customer',
            name='cu_phonenumber',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]

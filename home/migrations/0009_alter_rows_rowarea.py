# Generated by Django 5.0.3 on 2024-06-04 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_slider_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rows',
            name='RowArea',
            field=models.CharField(choices=[('VIP', 'VIP'), ('balcony', 'balcony'), ('ground', 'ground')], default='ground', max_length=7),
        ),
    ]

# Generated by Django 5.0.3 on 2024-06-04 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_slider_concertid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='sliders/'),
        ),
    ]
# Generated by Django 5.0.3 on 2024-06-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_seat_sansid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='ConcertStatus',
            field=models.CharField(choices=[('Soldout', 'Soldout'), ('Active', 'Active'), ('ComingSoon', 'ComingSoon')], default='Active', max_length=20),
        ),
    ]

# Generated by Django 5.0.3 on 2024-05-21 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_sans_seatid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sans',
            name='SeatId',
        ),
    ]
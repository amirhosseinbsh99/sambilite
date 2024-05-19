# Generated by Django 5.0.3 on 2024-05-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_seat_seatnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='NumberofSeat',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='SeatArea',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='SeatPrice',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='SeatRow',
        ),
        migrations.AddField(
            model_name='rows',
            name='NumberofSeat',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rows',
            name='RowArea',
            field=models.CharField(blank=True, choices=[('VIP', 'VIP'), ('balcony', 'balcony'), ('ground', 'ground')], max_length=7),
        ),
    ]

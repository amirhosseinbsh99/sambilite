# Generated by Django 5.0.3 on 2024-05-09 18:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('ConcertId', models.AutoField(primary_key=True, serialize=False)),
                ('ConcertName', models.CharField(max_length=100)),
                ('ConcertType', models.CharField(choices=[('music', 'music'), ('show', 'show'), ('cinema', 'cinema')], default='music', max_length=10)),
                ('ConcertDate', models.DateTimeField(max_length=20)),
                ('ConcertAddress', models.CharField(blank=True, max_length=250)),
                ('ConcertImage', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('ConcertLocation', models.CharField(max_length=40)),
                ('ArtistName', models.CharField(max_length=100)),
                ('ConcertStatus', models.CharField(choices=[('Soldout', 'Soldout'), ('Active', 'Active'), ('ComingSoon', 'ComingSoon')], default='active', max_length=20)),
                ('NumberRows', models.IntegerField()),
                ('NumberSeatsInRows', models.IntegerField()),
                ('RowPrice', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sans',
            fields=[
                ('SansId', models.AutoField(primary_key=True, serialize=False)),
                ('SansNumber', models.IntegerField(blank=True)),
                ('SansTime', models.TimeField()),
                ('ConcertId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.concert')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('SeatId', models.AutoField(primary_key=True, serialize=False)),
                ('SeatArea', models.CharField(blank=True, choices=[('VIP', 'VIP'), ('balcony', 'balcony'), ('ground', 'ground')], max_length=7)),
                ('SeatRow', models.IntegerField()),
                ('SeatNumber', models.IntegerField(blank=True, null=True)),
                ('SeatStatus', models.CharField(choices=[('Empty', 'Empty'), ('Reserved', 'Reserved'), ('Reserving', 'Reserving'), ('not_buyable', 'not_buyable'), ('selected', 'selected')], default='Empty', max_length=20)),
                ('SeatPrice', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('ConcertId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Concert_name', to='home.concert')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('TicketId', models.AutoField(primary_key=True, serialize=False)),
                ('Ticket_Serial', models.CharField(max_length=15)),
                ('ConcertId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.concert')),
                ('SansId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.sans')),
                ('SeatId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.seat')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('PaymentId', models.AutoField(primary_key=True, serialize=False)),
                ('PaymentDate', models.DateTimeField(auto_now_add=True)),
                ('PaymentStatus', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed'), ('canceled', 'canceled')], default='Pending', max_length=9)),
                ('CustomerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('SeatId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.seat')),
                ('TicketId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ticket')),
            ],
        ),
    ]

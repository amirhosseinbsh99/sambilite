# Generated by Django 5.0.3 on 2024-04-21 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('co_id', models.AutoField(primary_key=True, serialize=False)),
                ('co_name', models.CharField(max_length=100)),
                ('co_type', models.CharField(choices=[('music', 'music'), ('show', 'show'), ('cinema', 'cinema')], default='music', max_length=10)),
                ('co_date', models.DateTimeField(max_length=20)),
                ('co_address', models.CharField(blank=True, max_length=250)),
                ('co_seats', models.IntegerField(blank=True)),
                ('co_image', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('co_location', models.CharField(max_length=40)),
                ('a_name', models.CharField(max_length=100)),
                ('co_status', models.CharField(choices=[('Soldout', 'Soldout'), ('Active', 'Active'), ('ComingSoon', 'ComingSoon')], default='active', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sans',
            fields=[
                ('sa_id', models.AutoField(primary_key=True, serialize=False)),
                ('sa_number', models.IntegerField(blank=True)),
                ('sa_time', models.TimeField()),
                ('co_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.concert')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('se_id', models.AutoField(primary_key=True, serialize=False)),
                ('se_area', models.CharField(blank=True, choices=[('VIP', 'VIP'), ('balcony', 'balcony'), ('simple', 'simple')], max_length=7)),
                ('se_row', models.IntegerField(blank=True)),
                ('se_number', models.IntegerField(blank=True)),
                ('se_status', models.CharField(choices=[('Empty', 'Empty'), ('Reserved', 'Reserved'), ('Reserving', 'Reserving'), ('noy_buyable', 'noy_buyable')], default='Empty', max_length=20)),
                ('se_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('se_min_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('se_max_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('co_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.concert')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('t_id', models.AutoField(primary_key=True, serialize=False)),
                ('t_serial', models.CharField(max_length=15)),
                ('co_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.concert')),
                ('sa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sans')),
                ('se_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.seat')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed'), ('canceled', 'canceled')], default='Pending', max_length=9)),
                ('se_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.seat')),
                ('t_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ticket')),
            ],
        ),
    ]

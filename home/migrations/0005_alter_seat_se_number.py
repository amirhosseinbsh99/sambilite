# Generated by Django 5.0.3 on 2024-04-21 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_seat_se_max_price_remove_seat_se_min_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='se_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
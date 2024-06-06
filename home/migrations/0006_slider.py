# Generated by Django 5.0.3 on 2024-06-04 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_concert_concertstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='slider/images/')),
                ('url', models.URLField(blank=True)),
            ],
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-17 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_post_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='b_type',
            field=models.CharField(choices=[], max_length=9),
        ),
    ]

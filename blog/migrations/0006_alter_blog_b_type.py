# Generated by Django 5.0.3 on 2024-04-17 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blog_seocanonical_alter_blog_seodescription_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='b_type',
            field=models.CharField(max_length=50),
        ),
    ]

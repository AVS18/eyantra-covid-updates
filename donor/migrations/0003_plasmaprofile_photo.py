# Generated by Django 3.1.2 on 2021-05-24 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0002_donorrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='plasmaprofile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='plasma_donors'),
        ),
    ]

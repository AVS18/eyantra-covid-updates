# Generated by Django 3.1.2 on 2021-05-24 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_auto_20210524_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='fee',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
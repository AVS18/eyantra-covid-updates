# Generated by Django 3.1.2 on 2021-05-24 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='patient.bill'),
            preserve_default=False,
        ),
    ]

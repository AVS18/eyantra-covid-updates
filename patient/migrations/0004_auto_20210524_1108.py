# Generated by Django 3.1.2 on 2021-05-24 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_medicalreport_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalreport',
            name='report',
            field=models.ManyToManyField(blank=True, null=True, to='patient.Report'),
        ),
    ]

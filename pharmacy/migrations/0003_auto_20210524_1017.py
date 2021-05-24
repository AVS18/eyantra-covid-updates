# Generated by Django 3.1.2 on 2021-05-24 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_bill_status'),
        ('pharmacy', '0002_order_billing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='billing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.bill'),
        ),
        migrations.AlterField(
            model_name='order',
            name='medicine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pharmacy.medicine'),
        ),
    ]
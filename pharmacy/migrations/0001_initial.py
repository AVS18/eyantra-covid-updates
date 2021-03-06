# Generated by Django 3.1.2 on 2021-05-23 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2048)),
                ('image', models.ImageField(upload_to='medicines')),
                ('description', models.CharField(max_length=2048)),
                ('cost', models.IntegerField()),
                ('expiry_date', models.DateField()),
                ('expected_delivery', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Shipped', 'Shipped')], max_length=15)),
                ('tracking_id', models.CharField(blank=True, max_length=500, null=True)),
                ('service', models.CharField(blank=True, max_length=250, null=True)),
                ('receipt', models.ImageField(blank=True, null=True, upload_to='orders')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pharmacy.medicine')),
                ('ordered_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ordered_by', to=settings.AUTH_USER_MODEL)),
                ('ordered_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ordered_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

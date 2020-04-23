# Generated by Django 3.0.5 on 2020-04-23 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0005_auto_20200422_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='store_adress',
            field=models.CharField(default='17 rue de Paris - 75019', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='store_phone',
            field=models.CharField(default='06 59 68 98 54', max_length=255),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='VendorOpeningHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday', models.CharField(blank=True, default='-', max_length=100)),
                ('tuesday', models.CharField(blank=True, default='-', max_length=100)),
                ('wednesday', models.CharField(blank=True, default='-', max_length=100)),
                ('thursday', models.CharField(blank=True, default='-', max_length=100)),
                ('friday', models.CharField(blank=True, default='-', max_length=100)),
                ('saturday', models.CharField(blank=True, default='-', max_length=100)),
                ('sunday', models.CharField(blank=True, default='-', max_length=100)),
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Vendor.Vendor')),
            ],
        ),
    ]

# Generated by Django 3.0.5 on 2020-05-02 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Admin', '0001_initial'),
        ('Vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vendor.Vendor'),
        ),
    ]
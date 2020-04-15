# Generated by Django 3.0.5 on 2020-04-13 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20200412_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='vendor',
        ),
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Vendor',
        ),
    ]
# Generated by Django 3.0.5 on 2020-04-22 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0003_auto_20200422_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='description',
            field=models.TextField(default='Default description'),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.0.5 on 2020-04-21 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='website',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]

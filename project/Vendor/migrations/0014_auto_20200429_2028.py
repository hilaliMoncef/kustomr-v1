# Generated by Django 3.0.5 on 2020-04-29 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0013_auto_20200429_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramevent',
            name='date_published_char',
            field=models.CharField(default='01/05/2020', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='instagramevent',
            name='date_published',
            field=models.DateTimeField(),
        ),
    ]

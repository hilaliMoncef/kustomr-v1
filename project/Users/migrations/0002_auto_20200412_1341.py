# Generated by Django 3.0.5 on 2020-04-12 11:41

import Users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', Users.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='0661459943', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='store_type',
            field=models.CharField(choices=[('FOOD', 'Restaurant & bar'), ('SUPERMARKET', 'Supermarché')], default='FOOD', max_length=40),
        ),
        migrations.AddField(
            model_name='vendor',
            name='store_visits',
            field=models.CharField(choices=[('SM', 'Entre 50 et 200'), ('MD', 'Entre 200 et 500'), ('LG', 'Entre 500 et 1000'), ('XL', '1000+')], default='SM', max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]

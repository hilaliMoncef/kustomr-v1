# Generated by Django 3.0.5 on 2020-04-26 09:45

import Vendor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0008_auto_20200423_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.FileField(upload_to=Vendor.models.get_ig_upload_path)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('date_published', models.DateTimeField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ig_events', to='Vendor.Vendor')),
            ],
        ),
        migrations.CreateModel(
            name='FacebookEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.FileField(upload_to=Vendor.models.get_fb_upload_path)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('date_published', models.DateTimeField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fb_events', to='Vendor.Vendor')),
            ],
        ),
    ]
# Generated by Django 3.0.5 on 2020-05-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('responded', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_free', models.BooleanField(default=False)),
                ('link', models.CharField(max_length=400)),
                ('poster', models.FileField(blank=True, default=None, null=True, upload_to='tranings/posters/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

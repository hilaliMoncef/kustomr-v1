# Generated by Django 3.0.5 on 2020-04-16 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0003_auto_20200416_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('expiry', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
    ]
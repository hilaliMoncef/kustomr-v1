# Generated by Django 3.0.5 on 2020-05-05 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0005_smscampaign'),
        ('Customer', '0003_customerslist_mail_campaigns'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerslist',
            name='sms_campaigns',
            field=models.ManyToManyField(related_name='sms_lists', to='Vendor.MailCampaign'),
        ),
    ]

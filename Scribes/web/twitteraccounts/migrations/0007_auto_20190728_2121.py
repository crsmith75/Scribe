# Generated by Django 2.2.3 on 2019-07-28 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitteraccounts', '0006_twitteraccount_chainid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteraccount',
            name='chainid',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
# Generated by Django 2.2 on 2020-02-06 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Splunk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='splunk',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]
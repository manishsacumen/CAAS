# Generated by Django 2.2 on 2020-02-15 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Zendesk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zendeskmodel',
            name='url',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
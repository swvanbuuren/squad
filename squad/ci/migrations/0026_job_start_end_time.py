# Generated by Django 2.2.16 on 2020-11-13 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0025_backend_listen_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='testjob',
            name='ended_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='testjob',
            name='started_at',
            field=models.DateTimeField(null=True),
        ),
    ]
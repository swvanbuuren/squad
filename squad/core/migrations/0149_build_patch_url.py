# Generated by Django 2.2.16 on 2020-12-11 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0148_remove_legacy_storage_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='patch_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
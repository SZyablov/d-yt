# Generated by Django 4.0.10 on 2024-02-26 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0017_rename_ytdlpconfigs_ytdlppresets'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Preferences',
        ),
    ]

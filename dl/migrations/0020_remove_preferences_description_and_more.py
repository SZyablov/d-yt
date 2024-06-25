# Generated by Django 4.0.10 on 2024-02-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0019_preferences'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preferences',
            name='description',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='name',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='value',
        ),
        migrations.AddField(
            model_name='preferences',
            name='destination_folder',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='preferences',
            name='embed_chapters',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='preferences',
            name='embed_info_json',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='preferences',
            name='embed_metadata',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='preferences',
            name='embed_subtitles',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='preferences',
            name='subtitle_langs',
            field=models.CharField(default='en', max_length=32),
        ),
    ]

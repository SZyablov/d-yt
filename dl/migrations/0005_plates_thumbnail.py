# Generated by Django 4.0.10 on 2024-02-19 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0004_rename_downloadentries_plates'),
    ]

    operations = [
        migrations.AddField(
            model_name='plates',
            name='thumbnail',
            field=models.CharField(default='None', max_length=512),
        ),
    ]
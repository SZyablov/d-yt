# Generated by Django 4.0.10 on 2024-02-27 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0024_plates'),
    ]

    operations = [
        migrations.AddField(
            model_name='plates',
            name='internal_id',
            field=models.CharField(default='None', max_length=64),
        ),
    ]

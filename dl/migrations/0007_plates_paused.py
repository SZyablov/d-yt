# Generated by Django 4.0.10 on 2024-02-20 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0006_alter_plates_downloading'),
    ]

    operations = [
        migrations.AddField(
            model_name='plates',
            name='paused',
            field=models.BooleanField(default=False),
        ),
    ]
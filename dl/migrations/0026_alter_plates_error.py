# Generated by Django 4.0.10 on 2024-02-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0025_plates_internal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plates',
            name='error',
            field=models.CharField(max_length=128),
        ),
    ]

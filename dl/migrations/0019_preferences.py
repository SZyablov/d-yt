# Generated by Django 4.0.10 on 2024-02-26 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0018_delete_preferences'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('owner', models.CharField(default='', max_length=150)),
                ('name', models.CharField(default='', max_length=64)),
                ('value', models.CharField(default='', max_length=1024)),
                ('description', models.CharField(default='', max_length=1024)),
            ],
        ),
    ]

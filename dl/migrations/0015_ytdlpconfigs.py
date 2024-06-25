# Generated by Django 4.0.10 on 2024-02-26 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0014_preferences_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='YtdlpConfigs',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('owner', models.CharField(default='', max_length=150)),
                ('name', models.CharField(default='', max_length=64)),
                ('config', models.CharField(default='', max_length=1024)),
            ],
        ),
    ]
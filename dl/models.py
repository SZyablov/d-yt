from django.db import models

# Create your models here.
class Plates(models.Model):

    id = models.AutoField(primary_key=True)
    owner = models.CharField(default='', max_length=150)
    internal_id = models.CharField(default='None', max_length=64)
    video_id = models.CharField(default='None', max_length=64)
    title = models.CharField(default='None', max_length=128)
    options = models.CharField(default='None', max_length=128)
    format = models.CharField(default='None', max_length=128)
    filename = models.CharField(default='None', max_length=256)
    thumbnail = models.CharField(default='None', max_length=512)

    downloaded = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    eta = models.IntegerField(default=0)

    speed = models.FloatField(default=0.0)
    elapsed = models.FloatField(default=0.0)

    done = models.BooleanField(default=False)
    has_vcodec = models.BooleanField(default=False)
    downloading = models.BooleanField(default=False)
    paused = models.BooleanField(default=False)
    error = models.CharField(max_length=128)

class Preferences(models.Model):

    id = models.AutoField(primary_key=True)
    owner = models.CharField(default='', max_length=150)
    destination_folder = models.CharField(default='', max_length=1024)
    embed_thumbnail = models.BooleanField(default=False)
    embed_subtitles = models.BooleanField(default=False)
    subtitle_langs = models.CharField(default='en', max_length=32)
    embed_chapters  = models.BooleanField(default=False)
    embed_metadata  = models.BooleanField(default=False)
    embed_json_info = models.BooleanField(default=False)

class YtdlpPresets(models.Model):

    id = models.AutoField(primary_key=True)
    owner = models.CharField(default='', max_length=150)
    name = models.CharField(default='', max_length=64)
    config = models.CharField(default='', max_length=1024)
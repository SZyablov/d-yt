# ruff: noqa: E402
# ruff: noqa: F541

import django
django.setup()

from django.http import JsonResponse
import django.http
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Plates, Preferences, YtdlpPresets
from django.contrib.auth import authenticate, login, logout, get_user
from django.template.defaulttags import register
from .forms import LoginForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

import json
import yt_dlp
from multiprocessing import Process
import traceback
from functools import partial
import platform

# GLOSSARY:
#       plate - information about video download (quality, filesize, etc)
#      preset - settings to download video and/or audio of exact quality
# internal id - id for database, consists of youtube video id + choosen format ids
#               e.g. dQw4w9WgXcQ602139 (youtube id: dQw4w9WgXcQ, video format id: 602, audio format id: 139)



# video download processes
dl_processes = {}

# avaivalble formats for the last searched video
available_formats = {
    'video': {},
    'audio': {}
}
available_videos = {}
available_audios = {}

temp_infos = {}



# login page logic
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('watch')
                else:
                    messages.error(request,f'This account is disabled')
                    return render(request,'login.html',{'form': form})
            else:
                messages.error(request,f'Invalid username or password')
                return render(request,'login.html',{'form': form})
    else:
        form = LoginForm()

    if request.user.is_authenticated:
        return redirect('watch')
    
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):

    logout(request)
    messages.info(request, f'You have been successfully logged out. You can log-in again')

    return redirect('login')

# create preferences for the freshly created user
@receiver(post_save, sender=User)
def user_saved(sender, instance, **kwargs):

    if kwargs['created']:
        
        Preferences.objects.create(
                owner = instance.username,
                destination_folder = f'C:\\Users\\%username%\\Videos\\yt-kitchen\\' if platform.system() == 'Windows' else f'/home/%username%/yt-kitchen/',
            )



# main page where user can download video
@login_required
def watch(request):

    user = get_user(request)

    plates = reversed(list(Plates.objects.filter(owner=user).values()))
    presets = list(YtdlpPresets.objects.filter(owner=user))
    
    task_dict = {
        'plates': plates,
        'presets': presets
        }

    return render(request, 'yt-kitchen.html', context=task_dict)

# settings page
@login_required
def settings(request):

    user = get_user(request).username

    prefs = Preferences.objects.filter(owner=user)

    if len(prefs) == 0:
        Preferences.objects.create(
            owner=user,
            destination_folder = 'C:\\Users\\%username%\\Videos\\yt-kitchen\\')
        prefs = Preferences.objects.filter(owner=user)

    preferences = list(prefs.values())

    preferences_dict = {
        'preferences': preferences,
        }

    return render(request, 'yt-kitchen-settings.html', context=preferences_dict)

# presets page
@login_required
def ytdlppresets(request):

    configs = list(YtdlpPresets.objects.filter(owner=get_user(request).username))
    configs_dict = {
        'configs': configs,
        }

    return render(request, 'yt-kitchen-presets.html', context=configs_dict)



# i forgor what it does
# let it be here
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# change user settings
@login_required
def settingschange(request: django.http.HttpRequest):
    if request.method == 'POST':

        task = json.loads(request.body)
        
        user = get_user(request).username

        Preferences.objects.filter(owner=user).update(
            destination_folder  = task['destination_folder'],
            embed_thumbnail     = task['embed_thumbnail'],
            embed_subtitles     = task['embed_subtitles'],
            subtitle_langs      = task['subtitle_langs'] if 'subtitle_langs' in task else 'en',
            embed_chapters      = task['embed_chapters'],
            embed_metadata      = task['embed_metadata'],
            embed_json_info     = task['embed_json_info'],
        )

        return JsonResponse(task)



# code to format bytes into kilobytes, megabytes, etc.
def format_filesize(filesize: int):

    if not filesize:
        return '0'

    names = {
        0: 'bytes',
        1: 'KB',
        2: 'MB',
        3: 'GB',
        4: 'TB'
    }

    last_reduced = filesize
    reduced = filesize

    for i in range(1, len(names)+1):

        last_reduced = reduced
        reduced /= 1000

        if reduced < 0.9:
            return f'{last_reduced:.2f} {names[i-1]}'

# get available video and audio formats
def extract_formats(formats, username):

    available_formats[username] = {
       'video': {},
       'audio': {}
    }
    available_videos[username] = {}
    available_audios[username] = {}

    for f in formats:
        
        if 'mhtml' in f['ext']:
            continue

        ext = f['ext']
        height = f['height'] if 'height' in f else 0
        if 'fps' in f:
            fps = 0 if not f['fps'] else int(f['fps'])
        else:
            fps = 0
        resolution = f" {height}p{fps}" if height else ''

        abr = f" {int(f['abr'])}kbps" if f['abr'] else ''

        filesize = 0
        if 'filesize_approx' in f:
            filesize = f['filesize_approx'] if f['filesize_approx'] else filesize
        if 'filesize' in f:
            filesize = f['filesize'] if f['filesize'] else filesize

        filesize_formatted = format_filesize(int(filesize))
        if filesize_formatted == '0':
            filesize_formatted = '? bytes'

        if ext not in available_formats[username]['video']:
            available_formats[username]['video'][ext] = {}
        if ext not in available_formats[username]['audio']:
            available_formats[username]['audio'][ext] = {}

        if f['vcodec'] != 'none':
            if 'acodec' in f:
                if f['acodec'] != 'none': continue
            available_formats[username]['video'][ext][f'{resolution} ({filesize_formatted})'.strip()] = {
                'format': f['format_id'],
                'filesize': filesize
            }
        if 'acodec' in f:
            if f['acodec'] != 'none' and f['vcodec'] == 'none':
                available_formats[username]['audio'][ext][f'{abr} ({filesize_formatted})'.strip()] = {
                'format': f['format_id'],
                'filesize': filesize
            }

    for k, v in available_formats[username]['video'].items():
        available_videos[username].update({f'{k} {_format}':f for _format, f in v.items()})
    for k, v in available_formats[username]['audio'].items():
        available_audios[username].update({f'{k} {_format}':f for _format, f in v.items()})

# search for the videos
def make_search(url, preset = None):

    yt_opts_thumbnail = {
        'verbose': False,
        'write_thumbnail': True,
        'skip_download': True
    }
    if preset:
        yt_opts_thumbnail['format'] = preset

    with yt_dlp.YoutubeDL(yt_opts_thumbnail) as ydl:
        meta = ydl.extract_info(url, download=False)
        formats = meta.get('formats', [meta])

    return meta, formats

@login_required
def search(request: django.http.HttpRequest):
    if request.method == 'POST':

        task = json.loads(request.body)
        username = get_user(request).username
        
        meta, formats = make_search(task['url'])

        extract_formats(formats, username)
        
        task['title'] = meta['title']
        task['id'] = meta['id']

        if username not in temp_infos:
            temp_infos[username] = {}

        temp_infos[username][meta['id']] = meta

        with open('meta.json', 'w', encoding='utf8') as f:
            json.dump(meta, f, indent=2)
        
        task['videos'] = list(available_videos[username].keys())
        task['audios'] = list(available_audios[username].keys())

        return JsonResponse(task)



# download hook
def hook(id, username, dl_info: dict, d):

    if d['info_dict']['ext'] == 'vtt':
        return

    dl = Plates.objects.filter(owner=username, internal_id=id)

    dl.update(filename=d['filename'])

    if d['status'] == 'downloading':

        dl_info[d['info_dict']['format_id']] = d['downloaded_bytes']

        # TODO: VERY BAD, NEED TO CHANGE
        dl.update(
            downloaded=sum(list(dl_info.values())),
            # total=d['total_bytes'],
            eta=d['eta'] if d['eta'] else 0,
            speed=d['speed'] if d['speed'] else 0,
            elapsed=d['elapsed'],
            done=False
        )
        
    if d['status'] == 'finished':
        
        dl.update(filename=d['filename'])

        dl.update(
            downloading=False,
            done=True,
            speed=0
        )

# logger for yt-dlp
class Logger(object):
    owner = ''
    internal_id = ''
    
    def __init__(self, internal_id, owner):
        self.internal_id = internal_id
        self.owner = owner

    def debug(self, msg):
        # print(msg)
        pass

    def warning(self, msg):
        # print(msg)
        pass

    def error(self, msg):
        
        if 'Traceback (most recent call last)' in msg:
            return

        Plates.objects.filter(owner=self.owner, internal_id=self.internal_id).update(
            error='ERROR:' + msg.split('ERROR:[0m')[-1]
        )

# download video
# function for the new process to do it asynchronous
def download_video(*args):

    url             = args[0]
    format          = args[1]
    internal_id     = args[2]
    extension       = args[3]
    prefs           = args[4]
    username        = args[5]
    has_vcodec      = args[6]

    dl_info = {}
    prefs = prefs

    extended_hook = partial(hook, internal_id, username, dl_info)
    
    # destination_folder = Preferences.objects.get(name='Destination folder')
    yt_opts_dl = {
        'verbose': True,
        'outtmpl': prefs['destination_folder'] + f'%(title)s-{internal_id}-yt-kitchen.%(ext)s',
        'merge_output_format': extension,
        'format': format,
        'overwrites': True,
        # 'ratelimit': 1000000,
        'logger': Logger(internal_id, username),
        'progress_hooks': [extended_hook],
        'postprocessors': []
    }

    # thumbnails
    if prefs['embed_thumbnail']:
        yt_opts_dl['postprocessors'].append({
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': False,
            })
    
    # subtitles
    if prefs['embed_subtitles'] and has_vcodec:
        yt_opts_dl['postprocessors'].append({
            'already_have_subtitle': False, 
            'key': 'FFmpegEmbedSubtitle'
            })
        yt_opts_dl['writesubtitles'] = True
        yt_opts_dl['subtitleslangs'] = [lang.strip() for lang in prefs['subtitle_langs'].split(',')]

    # chapters, json, metadata
    yt_opts_dl['postprocessors'].append({'add_chapters': prefs['embed_chapters'],
                 'add_infojson': prefs['embed_json_info'],
                 'add_metadata': prefs['embed_metadata'],
                 'key': 'FFmpegMetadata'})
    
    with yt_dlp.YoutubeDL(yt_opts_dl) as ydl:
        ydl.download(url) # start download

# start downloading process
def start_download(dl: Plates, id: str, format: str, download_id: str, prefs, username, ext: str = 'mp4'):
    dl.downloading = True
    dl.save(force_update=True)

    dl_process = Process(target=download_video, args=["https://www.youtube.com/watch?v="+id, format, download_id, ext, prefs, username, dl.has_vcodec])
    dl_process.start()

    dl_processes[download_id] = dl_process
# get filesize from the video
def get_filesize(f):

    filesize = 0
    if 'filesize_approx' in f:
        filesize = f['filesize_approx'] if f['filesize_approx'] else filesize
    if 'filesize' in f:
        filesize = f['filesize'] if f['filesize'] else filesize

    return filesize 

# API endpoint for download start
@login_required
def download(request: django.http.HttpRequest):
    try:
        if request.method == 'POST':
            
            username = get_user(request).username

            task = json.loads(request.body)
            if 'ext' not in task:
                task['ext'] = '.mp4'
            task['ext'] = task['ext'].replace('.', '')

            result_format = 'bestvideo*+bestaudio/best'
            options = ' | '.join([f['format_note'] if 'format_note' in f else f"{f['height']}p" for f in temp_infos[username][task['id']]['requested_formats']])
            filesizes = [get_filesize(f) for f in temp_infos[username][task['id']]['requested_formats']]

            # get formats, choosen options and filesize to process it later
            if 'preset' not in task:
                video_format = available_videos[username][task['video']]['format'] if 'video' in task else None
                audio_format = available_audios[username][task['audio']]['format'] if 'audio' in task else None

                if video_format and audio_format:

                    result_format = f'{video_format}+{audio_format}'
                    options = ' | '.join([task['video'] , task['audio']])
                    filesizes = [available_videos[username][task['video']]['filesize'], available_audios[username][task['audio']]['filesize']]

                elif audio_format:

                    result_format = audio_format
                    options = task['audio']
                    filesizes = [available_audios[username][task['audio']]['filesize']]

                elif video_format:

                    result_format = video_format
                    options = task['video']
                    filesizes = [available_videos[username][task['video']]['filesize']]

                if result_format == 'bestvideo*+bestaudio/best':
                    format_for_id = ''.join([f['format_id'] for f in temp_infos[username][task['id']]['requested_formats']])
                else:
                    format_for_id = result_format.replace('+', '')
            # get formats, choosen options and filesize to show it to user
            else:

                meta, formats = make_search(task['id'], task['preset'])

                with open('result.json', 'w', encoding='utf8') as f:
                    json.dump(meta, f, indent=2)

                result_format = task['preset']
                
                if 'requested_formats' in meta:
                    _options = ' | '.join([f['format_note'] if 'format_note' in f else f"{f['height']}p" for f in meta['requested_formats']])
                    filesizes = [get_filesize(f) for f in meta['requested_formats']]
                    format_for_id = ''.join([f['format_id'] for f in meta['requested_formats']])
                    
                    video_format = None
                    for m in meta['requested_formats']:
                        if m['vcodec'] != 'none':
                            video_format = m['vcodec']

                else:
                    _options = meta['format_note'] if 'format_note' in meta else f"{meta['height']}p"
                    filesizes = [get_filesize(meta)]
                    format_for_id = meta['format_id']

                    video_format = meta['vcodec'] if meta['vcodec'] != 'none' else None

                options = f"Preset: {task['preset_name']} ({_options})" 
            
            total_filesize = 0
            if min(filesizes) != 0:
                total_filesize = sum(filesizes)

            download_id = f"{task['id']}{format_for_id}"

            if Plates.objects.filter(owner=username, internal_id=download_id).count() == 0:
                dl = Plates.objects.create(
                    owner=username,
                    internal_id=download_id
                )

                Plates.objects.filter(owner=username, internal_id=download_id).update(
                    title=temp_infos[username][task['id']]['title'],
                    video_id=task['id'],
                    total=total_filesize,
                    thumbnail=temp_infos[username][task['id']]['thumbnail'],
                    format=result_format,
                    options=options,
                    has_vcodec=video_format is not None
                    )
                
            dl = Plates.objects.get(
                owner=username,
                internal_id = download_id
            )
            if not dl.downloading:
                prefs = Preferences.objects.filter(owner=username).values()[0]
                start_download(dl, task['id'], result_format, download_id, prefs, username, task['ext'])

            task['video_id'] = task['id']
            task['id'] = download_id
            task['title'] = dl.title
            task['thumbnail'] = dl.thumbnail

            return JsonResponse(task)

    except:
        print(traceback.format_exc())

# update video downloading info
@login_required
def checkplate(request: django.http.HttpRequest):
    try:
        if request.method == 'POST':

            task = json.loads(request.body)

            username = get_user(request).username

            for t in task['ids']:
                dl = Plates.objects.get(
                    owner=username,
                    internal_id=t
                )
                
                task[t] = {
                    'title': dl.title,
                    'filename': dl.filename,
                    'downloaded': dl.downloaded,
                    'total': dl.total,
                    'eta': dl.eta,
                    'speed': dl.speed if not dl.paused else 'Paused',
                    'elapsed': dl.elapsed,
                    'done': dl.done,
                    'downloading': dl.downloading,
                    'options': dl.options,
                    'error': dl.error,
                }

            del task['ids']

            return JsonResponse(task)

    except:
        print(traceback.format_exc())
        pass

# start or pause download
@login_required
def startstop(request: django.http.HttpRequest):
    try:
        if request.method == 'POST':

            task = json.loads(request.body)
            
            username = get_user(request).username

            dl = Plates.objects.filter(
                owner=username,
                internal_id=task['id']
            )[0]

            if dl.downloading:
                
                if task['id'] in dl_processes:
                    dl_processes[task['id']].kill()
                    del dl_processes[task['id']]

                dl.downloading = False
                dl.paused = True
                dl.speed = 0
                dl.save(force_update=True)

                task['result'] = 'stopped'

            else:
                
                prefs = Preferences.objects.filter(owner=username).values()[0]
                start_download(dl, dl.video_id, dl.format, task['id'], prefs, username)

                dl.paused = False
                dl.save(force_update=True)

                task['result'] = 'started'

            return JsonResponse(task)

    except:
        print(traceback.format_exc())

# delete video from list
@login_required
def delete(request: django.http.HttpRequest):
    try:
        if request.method == 'POST':

            task = json.loads(request.body)
            username = get_user(request).username

            Plates.objects.filter(
                owner=username,
                internal_id=task['id']
            ).delete()

            task['status'] = 'deleted'

            return JsonResponse(task)

    except:
        print(traceback.format_exc())

# save preset (new or existed)
@login_required
def savepreset(request: django.http.HttpRequest):
    try:
        if request.method == 'POST':

            task = json.loads(request.body)
            user = get_user(request)

            conf = YtdlpPresets.objects.update_or_create(
                owner=user.username,
                name=task['name']
            )[0]

            conf.config = task['config']
            conf.save(force_update=True)

            return JsonResponse(task)

    except:
        print(traceback.format_exc())

# delete preset
@login_required
def deletepreset(request: django.http.HttpRequest):
    try:
        if request.method == 'POST':

            task = json.loads(request.body)
            user = get_user(request)

            YtdlpPresets.objects.filter(
                owner=user.username,
                name=task['name']
            )[0].delete()

            return JsonResponse(task)

    except:
        print(traceback.format_exc())
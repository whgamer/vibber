from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm,ScheduleForm
from .models import Album, Song,Schedule


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)
def create_schedule1(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = ScheduleForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.schedule_name = request.POST['schedule_name']  # request.user request.schedule_name form.schedule_name
            # schedule.schedule_memo =  request.schedule_memo
            # file_type = album.album_logo.url.split('.')[-1]
            # file_type = file_type.lower()
            # if file_type not in IMAGE_FILE_TYPES:
            #     context = {
            #         'album': album,
            #         'form': form,
            #         'error_message': 'Image file must be PNG, JPG, or JPEG',
            #     }
            #     return render(request, 'music/create_album.html', context)
            schedule.save()
            return render(request, 'music/schedule_detail.html', {'schedule': schedule})
        context = {
            "form": form,
        }
        return render(request, 'music/create_schedule.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)

def create_schedule(request, schedule_id):
    form = ScheduleForm(request.POST or None)
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    if form.is_valid():
        # albums_songs = album.song_set.all()
        # for s in albums_songs:
        #     if s.song_title == form.cleaned_data.get("song_title"):
        #         context = {
        #             'album': album,
        #             'form': form,
        #             'error_message': 'You already added that song',
        #         }
        #         return render(request, 'music/create_song.html', context)
        schedule = form.save(commit=False)
        # schedule.schedule_name = album
        # song.audio_file = request.FILES['audio_file']
        # file_type = song.audio_file.url.split('.')[-1]
        # file_type = file_type.lower()
        # if file_type  in AUDIO_FILE_TYPES:
        #     context = {
        #         'album': album,
        #         'form': form,
        #         'error_message': 'Audio file must be WAV, MP3, or OGG',
        #     }
        #      return render(request, 'music/create_schedule.html', context)

        schedule.save()
        return render(request, 'music/schedule_detail.html', {'schedule': schedule})
    context = {
         'schedule': schedule,
        'form': form,
    }
    return render(request, 'music/create_schedule.html', context)
def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'albums': albums})


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})
def delete_schedule(request, schedule_id):
    # album = get_object_or_404(Album, pk=album_id)
    schedule = Schedule.objects.get(pk=schedule_id)
    schedule.delete()
    return render(request, 'music/detail.html', {'album': album})


def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'album': album, 'user': user})


def edit(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/edit.html', {'album': album, 'user': user})

# 编辑专辑 add  by  zyy 2018年7月31日
def edit_album(request,album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        album = get_object_or_404(Album, pk=album_id)
        form = AlbumForm(request.POST  or None)
        print('开始打印信息')
        # print(request.POST['album_artist'][0] )
        # form = AlbumForm(request.POST )
        print(album)
        # return render(request, 'music/schedule_detail.html', {'schedule': schedule, 'user': user})
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()
            print('保存成功')
        if request.method == "GET":
           return render(request,'music/login.html')
        else:
            # album = form.save(commit=False)
            album.id = request.POST.get('album_id')
            album.artist =  request.POST.get('album_artist')
            album.album_title =request.POST.get('album_title')
            album.genre =request.POST.get('album_genre')
            print(request.POST.get('album_title'))
            # album.album_logo = request.FILES['album_logo']
            # file_type = album.album_logo.url.split('.')[-1]
            # file_type = file_type.lower()
            # if file_type  in IMAGE_FILE_TYPES:
            #     context = {
            #         'album': album,
            #         'form': form,
            #         'error_message': 'Image file  be PNG, JPG, or JPEG',
            #     }
            #     return render(request, 'music/create_album.html', context)
            album.save()
            print('打印成功')
            return JsonResponse({'success': True})
            # return render(request, 'music/index', context)
            # return HttpResponseRedirect('/thanks/')
        # context = {
        #     # "form": form,
        # }
        return render(request,'更新失败')  #context 'music/edit.html'

def schedule_detail(request,schedule_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        schedule = get_object_or_404(Schedule, pk=schedule_id)
        return render(request, 'music/schedule_detail.html', {'schedule': schedule, 'user': user})

def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def schedules(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            schedule_ids = []

            for schedule in Schedule.objects.all():
                schedule_ids.append(schedule.pk)
                schedules_list = Schedule.objects.filter(pk__in=schedule_ids)
            if filter_by == 'favorites':
                users_songs = schedules_list.filter(is_favorite=True)
        except Schedule.DoesNotExist:
            users_songs = []
        return render(request, 'schedule/schedule.html', {
            'schedule_list': schedules_list,
            'filter_by': filter_by,
        })

def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        schedules_results = Schedule.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()

            schedules_results = schedules_results.filter(
                Q(schedules_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
                'schedules': schedules_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


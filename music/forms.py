from django import forms
from django.contrib.auth.models import User

from .models import Album, Song
from .models import Schedule


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']

class ScheduleForm(forms.ModelForm):
    schedule_date = forms.DateTimeField(label='预约日期')  # ,label='预约日期'
    schedule_name = forms.CharField( label='预约人姓名')
    schedule_telephone = forms.CharField( label='预约人电话')
    schedule_status = forms.CharField(label='预约状态')
    schedule_call = forms.IntegerField(label='电话次数')
    schedule_memo = forms.CharField( label='备注信息')
    class Meta:
        model = Schedule
        fields = ['schedule_name','schedule_date','schedule_telephone','schedule_status','is_favorite','schedule_call','schedule_memo']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

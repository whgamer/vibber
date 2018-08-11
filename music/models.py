from django.contrib.auth.models import Permission, User
from django.db import models
from django.utils.html import format_html
from django.contrib import admin

class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
class Schedule(models.Model):
    # schedule_id = models.Pr(Album, on_delete=models.CASCADE)
    schedule_date = models.DateTimeField(editable=True,verbose_name= '预约日期')   #,label='预约日期' ,label='预约人姓名',label='预约人电话' auto_now_add=True,
    schedule_name = models.CharField(max_length=20,verbose_name= '姓名')
    schedule_telephone = models.CharField(max_length=11,verbose_name= '移动电话')
    schedule_status = models.CharField(max_length=10,verbose_name= '状态')
    schedule_call = models.IntegerField(default=0,verbose_name= '电话次数')
    schedule_memo  = models.CharField(max_length=1000,verbose_name= '备注')
    is_favorite = models.BooleanField(default=False,verbose_name= '已做标记')
    user =models.CharField(max_length=10,default='all',verbose_name= '操作用户')
    def __str__(self):
        #返回值 加日期格式化
        return '客户姓名：'+self.schedule_name +' 预约日期'+str(self.schedule_date.strftime('%Y-%m-%d %H:%M:%S'))+'        电话号码：'+self.schedule_telephone
        # ,label='预约状态' ,label='电话次数' ,label='备注信息

    def colored_name(self):
        if self.schedule_status =='预约':
            color_code='green'
        elif self.schedule_status =='完成':
            color_code='yellow'
        else:
            color_code ='blue'
        return format_html(
            '<span style="color: #{};">{} </span>',
            color_code,
            self.schedule_status,
        )
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule_name', 'schedule_status', 'colored_name')
from django.contrib import admin
from .models import Album, Song,Schedule


admin.site.site_header = '四维彩超预约管理系统'
admin.site.site_title = '四维彩超预约'
# site_header = '四维彩超预约管理系统'  # 此处设置页面显示标题
# site_title = '四维彩超预约'  # 此处设置页面头部标题

class AlbumAdmin(admin.ModelAdmin):#设置选择对应的字段,并且分组显示信息
    fieldsets = [
        ('艺术家信息',{'fields' : ['user', 'artist']}),
        ('专辑风格',{'fields' : ['album_title', 'genre','is_favorite']  }),#,'classes': ['collapse'] 为每个fieldsets设置css类
    ]

admin.site.register(Album, AlbumAdmin)
# admin.site.register(Album)
admin.site.register(Song)
# class ScheduleAdmin(admin.ModelAdmin):#设置选择对应的字段,并且分组显示信息
#     # fields = ['schedule_date']
#     fieldsets = [
#         ('预约客户信息',{'fields' : [('schedule_name', 'schedule_telephone'),('schedule_date','is_favorite')]}),
#         ('预约信息',{'fields' : [('schedule_status', 'schedule_call'),'schedule_memo']  }),#,'classes': ['collapse'] 为每个fieldsets设置css类
#     ]
@admin.register(Schedule)#采用装饰器方式
class ScheduleAdmin(admin.ModelAdmin):    # ...
    list_display = ('schedule_name', 'schedule_telephone', 'schedule_date','is_favorite','schedule_status', 'schedule_call','colored_name')
    list_filter = ['schedule_date']
    search_fields = ['schedule_name','schedule_telephone']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    #ordering设置默认排序字段，负号表示降序排序
    ordering = ('-schedule_date',)
    #list_editable 设置默认可编辑字段
    list_editable = ['is_favorite',]# 'schedule_status'
    date_hierarchy = 'schedule_date'    # 详细时间分层筛选　
# class ChoiceInline(admin.TabularInline): #此处可以设置为 同时添加多行数据。

# admin.site.register(Schedule,ScheduleAdmin)


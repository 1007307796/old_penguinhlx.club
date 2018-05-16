from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.


class PostAdmin(admin.ModelAdmin):   # 定制管理后台，显示详细信息
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


admin.site.register(Post, PostAdmin)   # 注册管理员登陆模型
admin.site.register(Category)
admin.site.register(Tag)

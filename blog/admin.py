from django.contrib import admin
from .models import Post,Category,Tag
# Register your models here.


class AdminPost(admin.ModelAdmin):
    list_display = ['title','creat_time','modify_time','category','author']
admin.site.register(Post,AdminPost)
admin.site.register(Category)
admin.site.register(Tag)



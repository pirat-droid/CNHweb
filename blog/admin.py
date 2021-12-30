from django.contrib import admin
from blog.models import PostModel, TagModel, ImagePost


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'datetime_create', 'datetime_update']
    exclude = ['slug', ]


@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    exclude = ['slug', ]


@admin.register(ImagePost)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'image']
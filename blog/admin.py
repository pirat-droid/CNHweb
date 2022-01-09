from django.contrib import admin
from blog.models import (PostModel, TagModel, StaffModel, AuthorModel, ParagraphModel, CitationModel, CategoryTagModel,
                         SubscribeModel)


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'datetime_create', 'datetime_update']
    exclude = ['slug', ]


@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category']
    list_editable = ['category', 'slug']


@admin.register(StaffModel)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    exclude = ['slug', ]


@admin.register(AuthorModel)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'staff', 'image']
    exclude = ['slug', ]


@admin.register(ParagraphModel)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ['post', 'text']


@admin.register(CitationModel)
class CitationAdmin(admin.ModelAdmin):
    list_display = ['paragraph_id', 'paragraph', 'text']


@admin.register(CategoryTagModel)
class CategoryTagAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(SubscribeModel)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['email', 'datetime_create']
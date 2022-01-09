from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('post/<slug:url>/', PostPage.as_view(), name='post'),
    path('author/<slug:url>/', AuthorPage.as_view(), name='author'),
    path('tag/<slug:url>/', TagPage.as_view(), name='tag'),
    path('auto-add-post/', auto_add_post),
    path('about/', AboutPage.as_view(), name='about'),
    path('subscribe/', Subscribe.as_view(), name='subscribe'),
    path('all-news/', AllNewsPage.as_view(), name='all-news'),
]

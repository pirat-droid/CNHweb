import os
from datetime import datetime
import time
from django.db.models import Q
from django.http import HttpResponse
import authenticated
import requests
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.views.generic.list import MultipleObjectMixin
from bs4 import BeautifulSoup
from mtranslate import translate
from random import randint
import httplib2
from .models import TagModel, PostModel, ParagraphModel, CitationModel, AuthorModel, CategoryTagModel, SubscribeModel
from .forms import SubscribeForm
from .utils import DataMixin


class HomePage(DataMixin, TemplateView):
    template_name = 'cnh/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bitcoin_news'] = PostModel.objects.filter(tag__name='BITCOIN')[:5] .select_related('author')
        context['ethereum_news'] = PostModel.objects.filter(tag__name='ETHEREUM')[:5].select_related('author')
        context['nft_news'] = PostModel.objects.filter(tag__name='NFT')[:5].select_related('author')
        context['data_breach'] = PostModel.objects.filter(tag__name='DATA-BREACH')[:5].select_related('author')
        context['binance_news'] = PostModel.objects.filter(tag__name='BINANCE')[:5].select_related('author')
        context['regulation_news'] = PostModel.objects.filter(tag__name='РЕГУЛИРОВАНИЕ')[:5].select_related('author')
        context['altcoins_news'] = PostModel.objects.filter(tag__name='АЛЬТКОИНЫ')[:5].select_related('author')
        context['blockchain_news'] = PostModel.objects.filter(tag__name='БЛОКЧЕЙН')[:5].select_related('author')
        context['title'] = 'Главная новость'
        return dict(list(context.items()) + list(self.get_category().items()) + list(self.get_authors().items()))


class AllNewsPage(DataMixin, ListView):
    template_name = 'cnh/posts.html'
    model = PostModel
    paginate_by = 5
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все статьи'
        return dict(list(context.items()) + list(self.get_category().items()) + list(self.get_authors().items()))


class PostPage(DataMixin, DetailView):
    model = PostModel
    template_name = 'cnh/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'url'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['like_news'] = PostModel.objects.filter(tag=self.object.tag.all()[:1])[:2].select_related('author').prefetch_related('tag')
        context['last_post_author'] = PostModel.objects.filter(Q(author=self.object.author), ~Q(slug=self.object.slug)).order_by('-datetime_create')[:2].prefetch_related('tag')
        context['title'] = self.object.title
        return dict(list(context.items()) + list(self.get_category().items()) + list(self.get_authors().items()))


class AuthorPage(DataMixin, DetailView, MultipleObjectMixin):
    context_object_name = 'author'
    model = AuthorModel
    template_name = 'cnh/author.html'
    slug_url_kwarg = 'url'
    paginate_by = 5
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = PostModel.objects.filter(author_id=self.get_object())
        context = super(AuthorPage, self).get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'автор - ' + self.object.name
        return dict(list(context.items()) + list(self.get_category().items()) + list(self.get_authors().items()))


class TagPage(DataMixin, DetailView, MultipleObjectMixin):
    context_object_name = 'tag'
    model = TagModel
    template_name = 'cnh/posts.html'
    slug_url_kwarg = 'url'
    paginate_by = 5
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = PostModel.objects.filter(tag__name=self.get_object().name).order_by('-datetime_create')
        context = super(TagPage, self).get_context_data(object_list=object_list, **kwargs)
        context['title'] = self.object.name
        return dict(list(context.items()) + list(self.get_category().items()) + list(self.get_authors().items()))


class AboutPage(DataMixin, TemplateView):
    template_name = 'cnh/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        return dict(list(context.items()) + list(self.get_category().items()) + list(self.get_authors().items()))


class Subscribe(CreateView):
    model = SubscribeModel
    form_class = SubscribeForm
    success_url = '/' # отобразить страницу с информацией о подписки


def auto_add_post(request):
    if request.GET['key'] == authenticated.key_auto_add_post and request.GET['link'] is not None:
        try:
            req = requests.get(request.GET['link'])
            soup = BeautifulSoup(req.text, 'html.parser')
            element = soup.find('div', 'main col-sm-12')

            title = translate(element.find('h1', 'title21').text, 'ru')

            time_read = element.find('span', 'textdesc')
            time_read = time_read.text
            i = time_read.find(' ')
            time_read = time_read[:i]

            post = element.find('div', 'textbody')
            image = post.find('img')["src"]
            h = httplib2.Http('.cache')
            response, content = h.request(image.replace(' ', ''))
            path = f'post/title/{datetime.today().strftime("%Y")}/{datetime.today().strftime("%m")}/{datetime.today().strftime("%d")}/'
            image_name = f'{datetime.today().strftime("%Y-%m-%d-%H:%M:%S")}.jpg'
            try:
                out = open('media/' + path + image_name, 'wb')
            except FileNotFoundError:
                os.makedirs('media/' + path)
                out = open(path + image_name, 'wb')
            out.write(content)
            out.close()
            author_id = randint(2, 11)
            print(str(author_id))
            author = AuthorModel.objects.get(id=author_id)

            post_id = PostModel.objects.create(title=title, title_i=path + image_name, author=author, time_read=time_read).id

            paragraphs = post.find_all('p')
            for p in paragraphs:
                if p.find('img'):
                    pass
                if p.text[:1] == '"':
                    paragraph = ParagraphModel.objects.get(id=paragraph_id)
                    CitationModel.objects.create(text=translate(p.text, 'ru'), paragraph=paragraph)
                elif len(p.text) > 1:
                    paragraph_id = ParagraphModel.objects.create(text=translate(p.text, 'ru'), post_id=post_id).id
                time.sleep(5)

            tags = soup.find_all('button', 'btn tag-btn')
            for t in tags:
                slug = t.text.replace(' ', '-').replace('&', '')
                try:
                    tag = TagModel.objects.get(slug=slug)
                    post = PostModel.objects.get(id=post_id)
                    post.tag.add(tag)
                    post.save()
                except:
                    tag_name = translate(t.text, 'ru')
                    tag = TagModel.objects.create(name=tag_name, slug=slug)
                    post = PostModel.objects.get(id=post_id)
                    post.tag.add(tag)
                    post.save()
                    time.sleep(2)

            return HttpResponse(status=200)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)
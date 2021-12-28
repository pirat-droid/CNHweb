from django.db import models
from django.urls import reverse
from unidecode import unidecode
from django.template import defaultfilters


class Tag(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Название тега')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'таг'
        verbose_name_plural = 'теги'
        ordering = ['name']


class Post(models.Model):
    title = models.CharField(max_length=250,
                            unique=True,
                            verbose_name='Название поста')
    slug = models.SlugField(max_length=250,
                            unique=True,
                            db_index=True,
                            verbose_name='URL')
    title_i = models.ImageField(upload_to='post/title/%Y/%m/%d',
                                verbose_name='Титульное изображение')
    tag = models.ForeignKey(Tag,
                            on_delete=models.PROTECT,
                            verbose_name='таг')
    text = models.TextField(verbose_name='Текст поста')
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['datetime_create', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.title))
        return super().save(*args, **kwargs)


class ImagePost(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             verbose_name='Пост')
    image = models.ImageField(upload_to='post/imaage/%Y/%m/%d',
                              verbose_name='Путь хранения')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return self.post.title

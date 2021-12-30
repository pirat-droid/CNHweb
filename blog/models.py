from django.db import models
from django.urls import reverse
from unidecode import unidecode
from django.template import defaultfilters


class TagModel(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Название тега')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='URL')
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

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


class PostModel(models.Model):
    title = models.CharField(max_length=250,
                            unique=True,
                            verbose_name='Название поста')
    slug = models.SlugField(max_length=250,
                            unique=True,
                            db_index=True,
                            verbose_name='URL')
    title_i = models.ImageField(upload_to='post/title/%Y/%m/%d',
                                verbose_name='Титульное изображение')
    tag = models.ManyToManyField(TagModel,
                            verbose_name='таг')
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
    post = models.ForeignKey(PostModel,
                             on_delete=models.CASCADE,
                             verbose_name='Пост')
    image = models.ImageField(upload_to='post/image/%Y/%m/%d',
                              verbose_name='Путь хранения')
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return self.post.title


class AuthorModel(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='ФИО автора')
    staff = models.ForeignKey('StaffModel',
                              on_delete=models.PROTECT,
                              verbose_name='Должность')
    slug = models.SlugField(max_length=100,
                            unique=True,
                            db_index=True,
                            verbose_name='URL')
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', kwargs={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class StaffModel(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='ФИО автора')
    slug = models.SlugField(max_length=100,
                            unique=True,
                            db_index=True,
                            verbose_name='URL')
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('staff', kwargs={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class ParagraphModel(models.Model):
    post = models.ForeignKey(PostModel,
                             on_delete=models.CASCADE,
                             verbose_name='Пост')
    text = models.TextField(verbose_name='Текст')
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Абзац'
        verbose_name_plural = 'Абзацы'

    def __str__(self):
        return self.post.title


class CitationModel(models.Model):
    paragraph = models.ForeignKey(ParagraphModel,
                             on_delete=models.CASCADE,
                             verbose_name='Параграф')
    text = models.TextField(verbose_name='Текст')
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'

    def __str__(self):
        return self.paragraph.post.title


class CitationModel(models.Model):
    paragraph = models.ForeignKey(ParagraphModel,
                             on_delete=models.CASCADE,
                             verbose_name='Параграф')
    image = models.ImageField(upload_to='post/paragraph/image/%Y/%m/%d',
                              verbose_name='Путь хранения')
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'

    def __str__(self):
        return self.paragraph.post.title



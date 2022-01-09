from django.db import models
from django.urls import reverse
from unidecode import unidecode
from django.template import defaultfilters


class CategoryTagModel(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория тегов'
        verbose_name_plural = 'Категории тегов'
        ordering = ['name']


class TagModel(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Название тега')
    category = models.ForeignKey(CategoryTagModel,
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 related_name='tag',
                                 null=True,
                                 blank=True)
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

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = defaultfilters.slugify(unidecode(self.name))
    #     return super().save(*args, **kwargs)

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
    time_read = models.TextField(max_length=2,
                                 verbose_name='Время на чтение')
    tag = models.ManyToManyField(TagModel,
                            verbose_name='таг')
    author = models.ForeignKey("AuthorModel",
                               on_delete=models.CASCADE,
                               verbose_name="Автор поста")
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-datetime_create', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'url': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.title))
        return super().save(*args, **kwargs)


class AuthorModel(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='ФИО автора')
    image = models.ImageField(upload_to='author/image',
                              verbose_name='фото аналитика')
    biography = models.TextField(verbose_name='Биография')
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
                            verbose_name='Должность')
    slug = models.SlugField(max_length=100,
                            unique=True,
                            db_index=True,
                            verbose_name='URL',
                            blank=True)
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
                             verbose_name='Пост',
                             related_name='paragraph')
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
                             verbose_name='Параграф',
                             related_name='quo')
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


class SubscribeModel(models.Model):
    email = models.EmailField(db_index=True)
    datetime_create = models.DateTimeField(auto_now_add=True,
                                           db_index=True,
                                           verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True,
                                           verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return self.email




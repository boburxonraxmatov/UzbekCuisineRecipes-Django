from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name='Название категории')  # title VARCHAR(30)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок статьи')
    content = models.TextField(verbose_name='Содержание статьи')
    photo = models.ImageField(upload_to=f'photos/', verbose_name='Фотография', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    publish = models.BooleanField(default=True, verbose_name='Статус публикации')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    youtube = models.URLField(verbose_name='Видео с YouTube', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

    def get_photo(self):  # если у себя есть фото, то вернуть его url, иначе ссылка
        if self.photo:
            return self.photo.url
        else:
            return 'https://media-cldnry.s-nbcnews.com/image/upload/newscms/2019_01/2705191/nbc-social-default.png'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


"""Сделать модель комментария которая знает пользователя, 
Статью, свой текст, и дату создания
Реализовать вывод комментариев к статье
Реализовать форму для комментариев
Реализовать вывод формы на статью, если пользователь вошел в акк
Реализовать сохранение комментария"""


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    text = models.TextField(verbose_name='Комментарии')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.article.title} - {self.text[:20]}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    like = models.BooleanField(default=False, verbose_name='Лайк')
    dislike = models.BooleanField(default=False, verbose_name='Дизлайк')

    def __str__(self):
        return f'{self.article.title} - {self.user.username} - {self.like} - {self.dislike}'

    class Meta:
        verbose_name = 'Лайк или Дизлайк'
        verbose_name_plural = 'Лайки и Дизлайки'


# когда лайки дизлайки отдельно
# class Dislike(models.Model):
#    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
#    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
#    dislike = models.BooleanField(default=False, verbose_name='Дизлайк')
#
#    def __str__(self):
#       return f'{self.article.title} - {self.user.username} - {self.dislike}'
#
#    class Meta:
#       verbose_name = 'Дизлайк'
#       verbose_name_plural = 'Дизлайки'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Фото пользователя')

    def get_photo(self):  # если у себя есть фото, то вернуть его url, иначе ссылка
        if self.photo:
            return self.photo.url
        else:
            return 'https://www.seekpng.com/png/detail/966-9665493_my-profile-icon-blank-profile-image-circle.png'

    def __str__(self):
        return f'{self.user.username} - {self.photo}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

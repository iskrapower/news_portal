from django.db import models
from django.contrib.auth import get_user_model


class Article(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=4000, null=False, blank=False, verbose_name='Описание')
    author = models.ForeignKey(get_user_model(), related_name='authored_articles', on_delete=models.CASCADE, verbose_name='Автор')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации статьи')
    edited_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления статьи')
    image = models.ImageField(null=True, blank=True, upload_to='article_pics', default='article_pics/default_article.png', verbose_name='Картина')
    topics = models.ManyToManyField('newsfeed.Topic', related_name='article_set', blank=True)

    def __str__(self):
        return "{}. {}".format(self.id, self.title)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey('newsfeed.Article', related_name='comments', on_delete=models.CASCADE, verbose_name='Статья')
    text = models.TextField(max_length=4000, null=False, blank=False, verbose_name='Комментарий')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации комментария')
    edited_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время обновления комментария')

    def __str__(self):
        return self.text[:20]
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    

class Topic(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Название')
    description = models.TextField(max_length=4000, null=False, blank=False, verbose_name='Описание')
    author = models.ForeignKey(get_user_model(), related_name='authored_topics', on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания темы')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name="URL", null=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts_author',
                               verbose_name='Автор'
                               )
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name='posts_group',
                              blank=True, null=True,
                              verbose_name='Группа',
                              help_text='Выберите группу'
                              )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='groups'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Посты'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Ссылка', unique=True)
    description = models.TextField('Описание')

    class Meta:
        db_table = 'Форум'
        verbose_name = 'Группы'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Комментарий.',
        help_text='Напишите текст комментария')
    created = models.DateTimeField(
        'Дата', auto_now_add=True
    )

    class Meta:
        db_table = 'Comment'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name='following'
    )

    class Meta:
        db_table = 'Follow'
        unique_together = ['user', 'author']
        constraints = [
            models.CheckConstraint(check=~models.Q(user=models.F('author')),
                                   name='user_is_not_author')]

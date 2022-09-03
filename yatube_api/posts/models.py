from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=100,
        unique=True
    )
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    MESSAGE_FORM = (
        'Дата публикации: {}, '
        'автор: {}, '
        'группа: {}, '
        'пост: {:.15}.'
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    class Meta():
        ordering = ('pub_date',)

    def __str__(self):
        return self.MESSAGE_FORM.format(
            self.pub_date,
            self.author.username,
            self.group,
            self.text
        )


class Comment(models.Model):
    MESSAGE_FORM = (
        'Пост: {:.15}, '
        'автор комментария: {}, '
        'текст: {:.15}, '
        'дата создания: {}.'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.MESSAGE_FORM.format(
            self.post.text,
            self.author.username,
            self.text,
            self.created
        )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_object'
            ),
        ]

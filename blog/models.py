from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from category.models import Category

User = get_user_model()


class Post(models.Model):
    """Model definition for Post."""

    title = models.CharField(max_length=100, )

    short_description = models.CharField(max_length=100, )

    content = models.TextField()

    excerpt = models.TextField()

    slug = models.SlugField(max_length=150, )

    featured_image = models.URLField()

    date_posted = models.DateTimeField(default=timezone.now, )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='post',
    )

    class Meta:
        """Meta definition for Post."""

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Unicode representation of Post."""
        return str(f'{self.slug}')

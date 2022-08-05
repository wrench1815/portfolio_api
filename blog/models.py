from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

from category.models import Category

User = get_user_model()


class Post(models.Model):
    """Model definition for Post."""

    title = models.CharField(max_length=100, )

    short_description = models.CharField(max_length=100, )

    content = models.TextField()

    excerpt = models.TextField()

    slug = models.SlugField(
        max_length=150,
        editable=False,
    )

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


@receiver(post_save, sender=Post)
def add_post_slug(sender, instance, *args, **kwargs):
    post_slug = str(f'{instance.title} {instance.id}')
    post_slug = slugify(post_slug)

    Post.objects.filter(id=instance.id).update(slug=post_slug)

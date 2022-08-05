from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=100,
        editable=False,
    )

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return str(f'{self.slug}')


@receiver(post_save, sender=Category)
def add_cat_slug(sender, instance, *args, **kwargs):
    cat_slug = str(f'{instance.name} {instance.id}')
    cat_slug = slugify(cat_slug)

    Category.objects.filter(id=instance.id).update(slug=cat_slug)

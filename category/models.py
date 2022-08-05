from django.db import models


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(max_length=100, )

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        pass

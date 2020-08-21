from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50,
                            db_index=True)
    slug = models.SlugField(max_length=50,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('shop:category_list',
                       kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name="products",
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/',
                              blank=True,
                              null=True)
    description = models.TextField()
    brief = models.CharField(max_length=200,
                             blank=True,
                             null=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)

    class Meta:
        ordering = ('name',)
        index_together = ('id', 'slug')

    def get_absolute_url(self):
        return reverse('shop:detail',
                       kwargs={'pk': self.pk,
                               'slug': self.slug})

    def __str__(self):
        return self.name

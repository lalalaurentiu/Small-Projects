from django.db import models
from django.urls import reverse 

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(blank=True, upload_to="media/category")

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',  args=[self.slug]) 

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, upload_to="media/products")

    class Meta:
        verbose_name_plural = 'Products'

    def get_absolute_url(self):
        return reverse('shop:product_detail',  args=[self.slug])

    def __str__(self):
        return self.name


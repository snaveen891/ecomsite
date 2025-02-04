from django.db import models
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['category']),
            models.Index(fields=['-date_added']),
        ]

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.name
    
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL , related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product review'
        verbose_name_plural = 'product reviews'
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
            models.Index(fields=['-date_added']),
        ]

    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'


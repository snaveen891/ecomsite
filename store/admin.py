from django.contrib import admin

from .models import Category, Product, ProductReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'date_added']
    list_filter = ['available', 'date_added']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'date_added']
    list_filter = ['date_added']
    search_fields = ['product', 'user']
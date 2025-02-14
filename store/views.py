from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.db import models
from .forms import ProductReviewForm, SearchForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = cache.get('all_products')
    if not products:
        products = Product.objects.filter(available=True)
        cache.set('all_products', products)
    search_form = SearchForm()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if category:
        cache_key = category.slug
    else:
        cache_key = 'all'
    return render(request, 'store/product/list.html', {'category': category, 'categories': categories, 'products': products, 'search_form': search_form, 'cache_key': cache_key})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    product_rating = product.reviews.aggregate(models.Avg('rating'))['rating__avg']
    product_reviews = product.reviews.order_by('-date_added')[:3]
    cart_product_form = CartAddProductForm()
    review_form = ProductReviewForm()
    has_bought = False
    if request.user.is_authenticated:
        has_bought = request.user.orders.filter(items__product=product, status='D').exists()
    return render(request, 'store/product/detail.html', {'product': product, 'cart_product_form': cart_product_form, 'product_rating': product_rating, 'product_reviews': product_reviews, 'has_bought': has_bought, 'review_form': review_form})

def get_reviews(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    reviews = product.reviews.all()
    return render(request, 'store/product/reviews.html', {'product': product, 'reviews': reviews})

@login_required
def post_review(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        old_review = product.reviews.filter(user=request.user)
        if old_review.exists():
            old_review.delete()
        product.reviews.create(rating=rating, comment=comment, user=request.user)
    return redirect('store:product_detail', id=id, slug=slug)

def product_search(request):
    category = None
    categories = Category.objects.all()
    products = cache.get('all_products')
    if not products:
        products = Product.objects.filter(available=True)
        cache.set('all_products', products)
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            search_vector = SearchVector('name', weight='A') + SearchVector('description', weight='A') + SearchVector('category__name', weight='B') + SearchVector('category__description', weight='B')
            search_query = SearchQuery(query)
            products = products.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query, rank__gte=0.3).order_by('-rank')
    
    cache_key = f'search_{query}'    
    return render(request, 'store/product/list.html', {'category': category, 'categories': categories, 'products': products, 'search_form': search_form, 'query': query, 'cache_key': cache_key})

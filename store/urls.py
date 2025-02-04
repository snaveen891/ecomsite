from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/reviews/', views.get_reviews, name='product_reviews'),
    path('<int:id>/<slug:slug>/post_review/', views.post_review, name='post_review'),
    path('search/', views.product_search, name='product_search'),
]
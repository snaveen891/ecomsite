from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/' ,views.create_order, name='create_order'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment/fverify/<int:order_id>/', views.frontend_verify, name='fverify'),
    path('payment/verify', views.webhook_verify, name='bverify'),
    path('order_completed/<int:order_id>/', views.order_completed, name='order_completed'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order_failed/<int:order_id>/', views.order_failed, name='order_failed'),
]

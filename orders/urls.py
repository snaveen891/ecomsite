from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/' ,views.create_order, name='create_order'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment/fverify/', views.frontend_verify, name='fverify'),
    path('payment/verify', views.webhook_verify, name='bverify'),
    path('payment/done/', views.payment_done, name='payment_done'),
]

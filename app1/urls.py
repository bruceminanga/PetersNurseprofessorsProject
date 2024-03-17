from django.urls import path, include
from app1 import views


app_name = 'app1'
urlpatterns = [
    path('', views.home, name='home'),
    path('Order/', views.orderform, name='order'),
    path('process-payment/', views.process_payment, name='process_payment'),
    #path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('apply/', views.cart_detail, name='apply'),
    
]
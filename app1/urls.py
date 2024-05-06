from django.urls import path, include
from app1 import views
from .views import CouponView



app_name = 'app1'
urlpatterns = [
    path('', views.home, name='home'),
    path('api/coupons/<str:code>', CouponView.as_view()),
    path('Order/', views.orderform, name='order'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]

from django.urls import path, include
from app1 import views
from .views import CouponView, wallet_management_view, my_discounts_view, referral_earnings_view, messages_view, cancelled_orders, approved_orders, revision_orders, completed_orders, editing_orders, in_progress_orders, bidding_orders



app_name = 'app1'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/coupons/<str:code>', CouponView.as_view()),
    path('Order/', views.orderform, name='order'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('wallet-management/', wallet_management_view, name='wallet_management'),
    path('my-discounts/', my_discounts_view, name='my_discounts'),
    path('referral-earnings/', referral_earnings_view, name='referral_earnings'),
    path('messages/', messages_view, name='messages'),
    path('cancelled-orders/', cancelled_orders, name='cancelled_orders'),
    path('approved-orders/', approved_orders, name='approved_orders'),
    path('revision-orders/', revision_orders, name='revision_orders'),
    path('completed-orders/', completed_orders, name='completed_orders'),
    path('editing-orders/', editing_orders, name='editing_orders'),
    path('in-progress-orders/', in_progress_orders, name='in_progress_orders'),
    path('bidding-orders/', bidding_orders, name='bidding_orders'),

]

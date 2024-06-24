from django.urls import path, include
from app1 import views
from .views import (
    CouponView,
    wallet_management_view,
    my_discounts_view,
    referral_earnings_view,
    messages_view,
    cancelled_orders,
    revision_orders,
    unpaid_orders,
    editing_orders,
    in_progress_orders,
    bidding_orders,
    run_migrations,
    cancel_order,
    order_detail,
    order_bids,
    view_bid,
    accept_bid,
    reject_bid,

)


app_name = "app1"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/coupons/<str:code>", CouponView.as_view()),
    path("Order/", views.orderform, name="order"),
    path("process-payment/", views.process_payment, name="process_payment"),
    path("payment-cancelled/", views.payment_canceled, name="payment_cancelled"),
    path("wallet-management/", wallet_management_view, name="wallet_management"),
    path("my-discounts/", my_discounts_view, name="my_discounts"),
    path("referral-earnings/", referral_earnings_view, name="referral_earnings"),
    path("messages/", messages_view, name="messages"),
    path("cancelled-orders/", cancelled_orders, name="cancelled_orders"),
    path("revision-orders/", revision_orders, name="revision_orders"),
    path("unpaid-orders/", unpaid_orders, name="unpaid_orders"),
    path("editing-orders/", editing_orders, name="editing_orders"),
    path("in-progress-orders/", in_progress_orders, name="in_progress_orders"),
    path("bidding-orders/", bidding_orders, name="bidding_orders"),
    path("run-migrations/", run_migrations, name="run-migrations"),
    path("cancel-order/<int:order_id>/", views.cancel_order, name='cancel_order'),  
    path("order_detail/<int:order_id>/", views.order_detail, name="order_detail"),


    path("order-bids/<int:order_id>/", views.order_bids, name="order_bids"),
    path("view-bid/<int:bid_id>/", views.view_bid, name="view_bid"),
    path("accept-bid/<int:bid_id>/", views.accept_bid, name="accept_bid"),
    path("reject-bid/<int:bid_id>/", views.reject_bid, name="reject_bid"),

    path('writer/dashboard/', views.writer_dashboard, name='writer_dashboard'),
]

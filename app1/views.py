# Django imports
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

# Application-specific imports
from app1.forms import NewOrderForm, CouponApplyForm, NewsletterForm
from app1.models import Order, Message, Coupon, Referral, Wallet, Transaction, Discount

# Other Python imports
import os
from decimal import Decimal

@login_required
@require_POST
def view_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, order__writer=request.user)
    # Return bid details as JSON
    return JsonResponse({"bid": bid.to_dict()})

@login_required
@require_POST
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, order__writer=request.user)
    # Implement bid acceptance logic
    return JsonResponse({"success": True, "message": "Bid accepted successfully"})

@login_required
@require_POST
def reject_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, order__writer=request.user)
    # Implement bid rejection logic
    return JsonResponse({"success": True, "message": "Bid rejected successfully"})

@login_required
def order_bids(request, order_id):
    order = get_object_or_404(Order, id=order_id, writer=request.user)
    bids = order.bids.all()
    return render(request, "dashboard/order_bids.html", {"order": order, "bids": bids})

@login_required
def bidding_orders(request):
    bidding_orders = Order.objects.filter(bidding=True)
    return render(request, "dashboard/bidding_orders.html", {"bidding_orders": bidding_orders})

@login_required
def in_progress_orders(request):
    in_progress_orders = Order.objects.filter(status="in_progress")
    return render(request, "dashboard/in_progress_orders.html", {"in_progress_orders": in_progress_orders})

@login_required
def editing_orders(request):
    editing_orders = Order.objects.filter(status="editing")
    return render(request, "dashboard/editing_orders.html", {"editing_orders": editing_orders})

@login_required
def unpaid_orders(request):
    unpaid_orders = Order.objects.filter(status="unpaid")
    return render(request, "dashboard/unpaid_orders.html", {"unpaid_orders": unpaid_orders})


@login_required
def revision_orders(request):
    revision_orders = Order.objects.filter(status="revision")
    return render(request, "dashboard/revision_orders.html", {"revision_orders": revision_orders})

from django.http import JsonResponse

import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Order, Writer

logger = logging.getLogger(__name__)

@login_required
@require_POST
def cancel_order(request, order_id):
    logger.info(f"Cancel order request received for order_id: {order_id}")
    try:
        order = Order.objects.get(id=order_id)
        if order.writer != request.user:
            logger.warning(f"User {request.user.id} attempted to cancel order {order_id} belonging to user {order.writer.id}")
            return JsonResponse({"success": False, "message": "You do not have permission to cancel this order."})
        
        if order.status == 'unpaid':
            order.status = 'cancelled'
            order.save()
            logger.info(f"Order {order_id} cancelled successfully")
            return JsonResponse({"success": True, "message": "Order cancelled successfully."})
        else:
            logger.warning(f"Attempt to cancel non-unpaid order: {order_id}")
            return JsonResponse({"success": False, "message": "Order cannot be cancelled."})
    except Order.DoesNotExist:
        logger.error(f"Order does not exist: {order_id}")
        return JsonResponse({"success": False, "message": "Order does not exist."})
    except Exception as e:
        logger.exception(f"Error cancelling order {order_id}: {str(e)}")
        return JsonResponse({"success": False, "message": "An error occurred while cancelling the order."})


def debug_view(request, order_id):
    return HttpResponse(f"Order ID: {order_id}")

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import WriterProfileForm

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import WriterProfileForm
from .models import Bid, Order, Writer
from .decorators import writer_required

@login_required
def become_writer(request):
    try:
        writer_profile = request.user.writer_profile
    except Writer.DoesNotExist:
        writer_profile = Writer(user=request.user)

    if request.method == 'POST':
        form = WriterProfileForm(request.POST, instance=writer_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_writer = True
            profile.save()
            return redirect('app1:writer_dashboard')
    else:
        form = WriterProfileForm(instance=writer_profile)
    return render(request, 'dashboard/become_writer.html', {'form': form})

@login_required
@writer_required
def writer_dashboard(request):
    writer = request.user.writer_profile
    bids = Bid.objects.filter(writer=writer)
    orders = Order.objects.filter(writer=writer)
    return render(request, 'dashboard/writer_dashboard.html', {'writer': writer, 'bids': bids, 'orders': orders})


@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'dashboard/order_detail.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, f"Order with ID {order_id} does not exist.")
        return redirect('app1:bidding_orders')


@login_required
def cancelled_orders(request):
    cancelled_orders = Order.objects.filter(status="cancelled")
    return render(request, "dashboard/cancelled_orders.html", {"cancelled_orders": cancelled_orders})

@login_required
def messages_view(request):
    messages = Message.objects.filter(user=request.user)
    unread_messages_count = messages.filter(is_read=False).count()
    context = {"messages": messages, "unread_messages_count": unread_messages_count}
    return render(request, "dashboard/messages.html", context)

@login_required
def referral_earnings_view(request):
    referrals = Referral.objects.filter(referrer=request.user).order_by("-date")
    total_earnings = referrals.aggregate(total=Sum("amount_earned"))["total"] or 0
    context = {"total_earnings": total_earnings, "referrals": referrals}
    return render(request, "dashboard/referral_earnings.html", context)

@login_required
def my_discounts_view(request):
    discounts = Discount.objects.filter(user=request.user).order_by("-expiry_date")
    context = {"discounts": discounts}
    return render(request, "dashboard/my_discounts.html", context)

@login_required
def wallet_management_view(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except ObjectDoesNotExist:
        wallet = Wallet.objects.create(user=request.user, balance=0.00)
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")
    context = {"wallet_balance": wallet.balance, "transactions": transactions}
    return render(request, "dashboard/wallet_management.html", context)

@login_required
def newsletter(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            messages.success(request, "You will receive email.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = NewsletterForm()
    form2 = CouponApplyForm()
    return render(request, "base.html", {"form": form, "form2": form2})

@csrf_exempt
def paypal_ipn(request):
    print(request.POST)  # For debugging, remove in production
    return HttpResponse()

class CouponView(View):
    def get(self, request, *args, **kwargs):
        code = self.kwargs.get("code")
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                return JsonResponse({"active": coupon.active, "discount": coupon.discount})
            else:
                return JsonResponse({"active": False})
        except Coupon.DoesNotExist:
            return JsonResponse({"active": False})

def home(request):
    return render(request, "index.html")

@login_required
def dashboard(request):
    user = request.user
    registration_date = user.date_joined

    unpaid_orders_count = Order.objects.filter(status="unpaid").count()
    bidding_orders_count = Order.objects.filter(bidding=True).count()
    in_progress_orders_count = Order.objects.filter(status="in_progress").count()
    editing_orders_count = Order.objects.filter(status="editing").count()
    revision_orders_count = Order.objects.filter(status="revision").count()
    approved_orders_count = Order.objects.filter(status="approved").count()
    cancelled_orders_count = Order.objects.filter(status="cancelled").count()

    unread_messages_count = Message.objects.filter(user=user, is_read=False).count()
    active_discounts_count = Coupon.objects.filter(active=True).count()
    total_referral_earnings = Referral.objects.aggregate(total=Sum("amount_earned"))["total"] or 0.00

    try:
        wallet_balance = Wallet.objects.get(user=user).balance
    except Wallet.DoesNotExist:
        wallet_balance = 0.00

    pending_payments = Order.objects.filter(status="pending")
    
    context = {
        "unpaid_orders_count": unpaid_orders_count,
        "bidding_orders_count": bidding_orders_count,
        "in_progress_orders_count": in_progress_orders_count,
        "editing_orders_count": editing_orders_count,
        "revision_orders_count": revision_orders_count,
        "approved_orders_count": approved_orders_count,
        "cancelled_orders_count": cancelled_orders_count,
        "unread_messages_count": unread_messages_count,
        "active_discounts_count": active_discounts_count,
        "total_referral_earnings": total_referral_earnings,
        "wallet_balance": wallet_balance,
        "registration_date": registration_date,
    }

    if "order_submitted" in request.session:
        messages.success(request, "Order request submitted successfully.")
        del request.session["order_submitted"]

    return render(request, "dashboard/dashboard.html", context)


@login_required
def orderform(request):
    coupon_apply_form = CouponApplyForm()
    if request.method == "POST":
        form = NewOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.price = calculate_order_price(form.cleaned_data)
            order.save()
            messages.success(request, "Order request submitted successfully.")
            form2 = CouponApplyForm(request.POST)
            if form2.is_valid():
                code = form2.cleaned_data["coupon_code"]
                now = timezone.now()
                try:
                    coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
                    request.session["coupon_id"] = coupon.id
                except Coupon.DoesNotExist:
                    request.session["coupon_id"] = None
            return redirect("app1:dashboard")
        else:
            messages.error(request, "Invalid form submission.")
            print(form.errors.as_data())
            print("POST data:", request.POST)
            print("FILES data:", request.FILES)
    else:
        form = NewOrderForm()
    context = {"form": form, "coupon_apply_form": coupon_apply_form}
    return render(request, "orderform.html", context=context)

def calculate_order_price(data):
    return 0.0  # Replace with actual calculation

def process_payment(request):
    request.session["order_id"] = "1"
    order_id = request.session.get("order_id", 1)
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "%.2f" % Decimal(order.total_cost()).quantize(Decimal(".01")),
        "item_name": "Order {}".format(order.id),
        "invoice": str(order.id),
        "currency_code": "USD",
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "payments/process_payment.html", {"order": order, "form": form})

def payment_done(request):
    return render(request, "payments/payment_done.html")

@csrf_exempt
def payment_canceled(request):
    return render(request, "payments/payment_cancelled.html")

def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cart.clear(request)
            request.session["order_id"] = o.id
            return redirect("process_payment")
    else:
        form = CheckoutForm()
    return render(request, "ecommerce_app/checkout.html", {"form": form})

def run_migrations(request):
    secret = request.GET.get('secret_token')
    if secret != os.environ.get('MIGRATION_SECRET'):
        return HttpResponseForbidden("Forbidden")
    call_command('run_migrations')
    return HttpResponse("Migrations run successfully.")

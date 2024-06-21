# Import necessary modules from Django and the application
from django.shortcuts import render, redirect
from app1.forms import NewOrderForm, CouponApplyForm
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from .models import (
    Order,
    Message,
    Coupon,
    Referral,
    Wallet,
    Transaction,
    Discount,
    Referral,
    Message,
)
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views import View
from django.http import JsonResponse
from .forms import NewsletterForm
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


@login_required
def bidding_orders(request):
    bidding_orders = Order.objects.filter(bidding=True)
    return render(
        request, "dashboard/bidding_orders.html", {"bidding_orders": bidding_orders}
    )


@login_required
def in_progress_orders(request):
    in_progress_orders = Order.objects.filter(status="in_progress")
    return render(
        request,
        "dashboard/in_progress_orders.html",
        {"in_progress_orders": in_progress_orders},
    )


@login_required
def editing_orders(request):
    editing_orders = Order.objects.filter(status="editing")
    return render(
        request, "dashboard/editing_orders.html", {"editing_orders": editing_orders}
    )


@login_required
def unpaid_orders(request):
    unpaid_orders = Order.objects.filter(status="completed")
    return render(
        request,
        "dashboard/unpaid_orders.html",
        {"unpaid_orders": unpaid_orders},
    )


@login_required
def revision_orders(request):
    revision_orders = Order.objects.filter(status="revision")
    return render(
        request, "dashboard/revision_orders.html", {"revision_orders": revision_orders}
    )


@login_required
def approved_orders(request):
    approved_orders = Order.objects.filter(status="approved")
    return render(
        request, "dashboard/approved_orders.html", {"approved_orders": approved_orders}
    )


@login_required
def cancelled_orders(request):
    cancelled_orders = Order.objects.filter(status="cancelled")
    return render(
        request,
        "dashboard/cancelled_orders.html",
        {"cancelled_orders": cancelled_orders},
    )


def messages_view(request):
    messages = Message.objects.filter(user=request.user)
    unread_messages = messages.filter(is_read=False)
    unread_messages_count = unread_messages.count()

    context = {
        "messages": messages,
        "unread_messages_count": unread_messages_count,
    }
    return render(request, "dashboard/messages.html", context)


def referral_earnings_view(request):
    referrals = Referral.objects.filter(referrer=request.user).order_by(
        "-date"
    )  # Adjust the model fields as necessary
    total_earnings = (
        referrals.aggregate(total=models.Sum("amount_earned"))["total"] or 0
    )
    context = {
        "total_earnings": total_earnings,
        "referrals": referrals,
    }
    return render(request, "dashboard/referral_earnings.html", context)


def my_discounts_view(request):
    discounts = Discount.objects.filter(user=request.user).order_by(
        "-expiry_date"
    )  # Adjust the model fields as necessary
    context = {
        "discounts": discounts,
    }
    return render(request, "dashboard/my_discounts.html", context)


def wallet_management_view(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Handle the case where the wallet does not exist
        wallet = Wallet.objects.create(user=request.user, balance=0.00)
    transactions = Transaction.objects.filter(user=request.user).order_by(
        "-date"
    )  # Adjust the model fields as necessary
    context = {
        "wallet_balance": wallet.balance,
        "transactions": transactions,
    }
    return render(request, "dashboard/wallet_management.html", context)


def newsletter(request):
    if request.method == "POST":
        form3 = NewsletterForm(request.POST)
        if form3.is_valid():
            email = form3.cleaned_data["email"]
            # Add email to your newsletter subscription list
            messages.success(request, "you will recieve email.")
        else:
            # If the forms are not valid, display an error message
            messages.error(request, "Invalid form submission.")
            # Print the form errors
            print(form.errors.as_data())

            # Create new blank forms
            form3 = NewsletterForm()

        # Handle the coupon form
        form2 = CouponApplyForm(request.POST)
    else:
        form3 = NewsletterForm()

    return render(request, "base.html", {"form3": form3})


# This function is called when PayPal sends a POST request after a payment is completed
@csrf_exempt
def paypal_ipn(request):
    # The data sent by PayPal can be accessed via request.POST
    # You can use this data to update your system, for example, to mark the order as paid
    print(request.POST)  # This is just for debugging, remove this in production
    return HttpResponse()


# This is a class-based view for handling coupon related requests
class CouponView(View):
    # This function is called when a GET request is made to this view
    def get(self, request, *args, **kwargs):
        # Get the coupon code from the URL parameters
        code = self.kwargs.get("code")
        try:
            # Try to get the coupon with the given code
            coupon = Coupon.objects.get(code=code)
            # Check if the coupon is valid
            if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                # If valid, return a JSON response with the coupon's active status and discount
                return JsonResponse(
                    {"active": coupon.active, "discount": coupon.discount}
                )
            else:
                # If not valid, return a JSON response indicating that the coupon is not active
                return JsonResponse({"active": False})
        except Coupon.DoesNotExist:
            # If the coupon does not exist, return a JSON response indicating that the coupon is not active
            return JsonResponse({"active": False})


# This function handles the home page of the website
def home(request):
    # Render the HTML template index.html
    return render(request, "index.html")


@login_required
def dashboard(request):
    user = request.user
    registration_date = user.date_joined
    unpaid_orders = Order.objects.filter(status="completed")
    in_progress_orders = Order.objects.filter(status="in_progress")
    unpaid_orders_count = Order.objects.filter(paid=False).count()
    bidding_orders_count = Order.objects.filter(bidding=True).count()
    in_progress_orders_count = Order.objects.filter(status="in_progress").count()
    editing_orders_count = Order.objects.filter(status="editing").count()
    unpaid_orders_count = Order.objects.filter(status="completed").count()
    revision_orders_count = Order.objects.filter(status="revision").count()
    approved_orders_count = Order.objects.filter(status="approved").count()
    cancelled_orders_count = Order.objects.filter(status="cancelled").count()
    unread_messages_count = Message.objects.filter(read=False).count()
    active_discounts_count = Coupon.objects.filter(active=True).count()
    total_referral_earnings = (
        Referral.objects.aggregate(total=Sum("amount_earned"))["total"] or 0.00
    )
    wallet_balance = 0.00
    if user.is_authenticated:
        try:
            wallet_balance = Wallet.objects.get(user=user).balance
        except Wallet.DoesNotExist:
            # Handle the case where the wallet does not exist
            wallet_balance = 0.00
    pending_payments = Order.objects.filter(status="pending")
    context = {
        "unpaid_orders": unpaid_orders,
        "in_progress_orders": in_progress_orders,
        "pending_payments": pending_payments,
        "unpaid_orders_count": unpaid_orders_count,
        "bidding_orders_count": bidding_orders_count,
        "in_progress_orders_count": in_progress_orders_count,
        "editing_orders_count": editing_orders_count,
        "unpaid_orders_count": unpaid_orders_count,
        "revision_orders_count": revision_orders_count,
        "approved_orders_count": approved_orders_count,
        "cancelled_orders_count": cancelled_orders_count,
        "unread_messages_count": unread_messages_count,
        "active_discounts_count": active_discounts_count,
        "total_referral_earnings": total_referral_earnings,
        "wallet_balance": wallet_balance,
        "registration_date": registration_date,
    }
    # Only add the success message on certain conditions, e.g., after form submission
    if "order_submitted" in request.session:
        messages.success(request, "Order request submitted successfully.")
        del request.session["order_submitted"]

    return render(request, "dashboard/dashboard.html", context)


# This function handles the order form page of the website
# The login_required decorator ensures that only logged-in users can access this page
@login_required
def orderform(request):
    coupon_apply_form = CouponApplyForm()
    if request.method == "POST":
        form = NewOrderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.price = calculate_order_price(form.cleaned_data)
            order.save()

            # Save the uploaded files to AdditionalMaterial model
            for f in request.FILES.getlist('additional_material'):
                AdditionalMaterial.objects.create(order=order, file=f)

            messages.success(request, "Order request submitted successfully.")

            # Handle the coupon form
            form2 = CouponApplyForm(request.POST)
            if form2.is_valid():
                code = form2.cleaned_data["coupon_code"]
                now = timezone.now()
                try:
                    coupon = Coupon.objects.get(
                        code__iexact=code,
                        valid_from__lte=now,
                        valid_to__gte=now,
                        active=True,
                    )
                    request.session["coupon_id"] = coupon.id
                except Coupon.DoesNotExist:
                    request.session["coupon_id"] = None

            return redirect("app1:dashboard")

        else:
            messages.error(request, "Invalid form submission.")
            print(form.errors.as_data())
    else:
        form = NewOrderForm()

    context = {"form": form, "coupon_apply_form": coupon_apply_form}
    return render(request, "orderform.html", context=context)


def calculate_order_price(data):
    # Define your price calculation logic here
    return 0.0  # Replace with actual calculation


# This function handles the payment process
def process_payment(request):
    # Get the order ID from the session
    request.session["order_id"] = "1"
    order_id = request.session.get("order_id", 1)
    # Get the order object from the database
    order = get_object_or_404(Order, id=order_id)
    # Get the host name
    host = request.get_host()

    # Create a dictionary with the PayPal payment details
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "%.2f" % Decimal(order.total_cost()).quantize(Decimal(".01")),
        "item_name": "Order {}".format(order.id),
        "invoice": str(order.id),
        "currency_code": "USD",
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
    }

    # Create a form instance with the PayPal payment details
    form = PayPalPaymentsForm(initial=paypal_dict)
    # Render the HTML template process_payment.html with the order and form data
    return render(
        request, "payments/process_payment.html", {"order": order, "form": form}
    )


# This function handles the page that is displayed when the payment is done
def payment_done(request):
    return render(request, "payments/payment_done.html")


# This function handles the page that is displayed when the payment is canceled
# The csrf_exempt decorator indicates that the view is not protected against cross-site request forgery attacks
@csrf_exempt
def payment_canceled(request):
    return render(request, "payments/payment_cancelled.html")


# This function handles the checkout page
def checkout(request):
    # If the request method is POST, it means the user has submitted the form
    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = CheckoutForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # If the form is valid, handle the form data
            cleaned_data = form.cleaned_data
            # Clear the cart
            cart.clear(request)
            # Save the order ID to the session
            request.session["order_id"] = o.id
            # Redirect to the process payment page
            return redirect("process_payment")
    else:
        # If the request method is not POST, create a blank form
        form = CheckoutForm()
        # Render the HTML template checkout.html with the form data
        return render(request, "ecommerce_app/checkout.html", locals())

# myapp/views.py
from django.http import HttpResponse, HttpResponseForbidden
from django.core.management import call_command
import os

def run_migrations(request):
    secret = request.GET.get('secret_token')
    if secret != os.environ.get('MIGRATION_SECRET'):
        return HttpResponseForbidden("Forbidden")
    call_command('run_migrations')
    return HttpResponse("Migrations run successfully.")


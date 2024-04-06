# Import necessary modules from Django and the application
from django.shortcuts import render, redirect 
from app1.forms import NewCustomerForm, CouponApplyForm
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from .models import Order, Coupon
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views import View
from django.http import JsonResponse


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
        code = self.kwargs.get('code')
        try:
            # Try to get the coupon with the given code
            coupon = Coupon.objects.get(code=code)
            # Check if the coupon is valid
            if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                # If valid, return a JSON response with the coupon's active status and discount
                return JsonResponse({'active': coupon.active, 'discount': coupon.discount})
            else:
                # If not valid, return a JSON response indicating that the coupon is not active
                return JsonResponse({'active': False})
        except Coupon.DoesNotExist:
            # If the coupon does not exist, return a JSON response indicating that the coupon is not active
            return JsonResponse({'active': False})


# This function handles the home page of the website
def home(request):
    # Render the HTML template index.html
    return render(request, "index.html")

# This function handles the order form page of the website
# The login_required decorator ensures that only logged-in users can access this page
@login_required
def orderform(request):
    # Create form instances
    
    coupon_apply_form = CouponApplyForm()  # Define here
    # If the request method is POST, it means the user has submitted the form
    if request.method == 'POST':
        form = NewCustomerForm(request.POST, request.FILES)
        # Check if the forms are valid
        if form.is_valid():
            # Save the form but don't commit to the database yet
            order = form.save(commit=False)
            # Assign the calculated price to the order's price field
            order.price = price
            # Now save the order to the database
            order.save()
            # Display a success message
            messages.success(request, 'Order request submitted successfully.')

           
        else:
            # If the forms are not valid, display an error message
            messages.error(request, 'Invalid form submission.')
            # Print the form errors
            print(form.errors.as_data())
            
            # Create new blank forms
            form = NewCustomerForm()
            
        # Handle the coupon form
        form2 = CouponApplyForm(request.POST) 
        if form2.is_valid():
            # If the form is valid, get the coupon code from the form
            code = form2.cleaned_data['coupon_code']
            now = timezone.now()
            try:
                # Try to get the coupon with the given code that is valid and active
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                # If the coupon exists, store the coupon id in the session
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                # If the coupon does not exist, set the coupon id in the session to None
                request.session['coupon_id'] = None    
    else:
        # If the request method is not POST, create blank forms
        form = NewCustomerForm()
        

    # Create a context dictionary to pass to the template
    context = {
        'form': form,
        'coupon_apply_form': coupon_apply_form
        
    }
    
    # Render the HTML template orderform.html with the data in the context variable
    return render(request, "orderform.html", context=context)

# This function handles the payment process
def process_payment(request):
    # Get the order ID from the session
    request.session['order_id'] = '1'
    order_id = request.session.get('order_id', 1)
    # Get the order object from the database
    order = get_object_or_404(Order, id=order_id)
    # Get the host name
    host = request.get_host()

    # Create a dictionary with the PayPal payment details
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % Decimal(order.total_cost()).quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
    }

    # Create a form instance with the PayPal payment details
    form=PayPalPaymentsForm(initial=paypal_dict)
    # Render the HTML template process_payment.html with the order and form data
    return render(request, 'payments/process_payment.html', {'order': order, 'form': form})

# This function handles the page that is displayed when the payment is done
def payment_done(request):
    return render(request, 'payments/payment_done.html')

# This function handles the page that is displayed when the payment is canceled
# The csrf_exempt decorator indicates that the view is not protected against cross-site request forgery attacks
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payments/payment_cancelled.html')

# This function handles the checkout page
def checkout(request):
    # If the request method is POST, it means the user has submitted the form
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = CheckoutForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # If the form is valid, handle the form data
            cleaned_data = form.cleaned_data
            # Clear the cart
            cart.clear(request)
            # Save the order ID to the session
            request.session['order_id'] = o.id
            # Redirect to the process payment page
            return redirect('process_payment')
    else:
        # If the request method is not POST, create a blank form
        form = CheckoutForm()
        # Render the HTML template checkout.html with the form data
<<<<<<< HEAD
        return render(request, 'ecommerce_app/checkout.html', locals())
=======
        return render(request, 'ecommerce_app/checkout.html', locals())
>>>>>>> bde3b02 (final commit)

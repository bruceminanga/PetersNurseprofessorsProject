from django.shortcuts import render, redirect 
from app1.forms import NewCustomerForm, CouponApplyForm
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from .models import Order, Coupon
from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
    
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.contrib import messages
# from .utils import calculate_price

from django.utils import timezone
from django.views.decorators.http import require_POST




def cart_detail(request):
    if request.method == 'POST':
        form2 = CouponApplyForm(request.POST)
        if form2.is_valid():
            # Handle the valid form data...
            pass
    else:
        form2 = CouponApplyForm()

    return render(request, 'index.html', {'form2': form2})

                  
                  
                   


# Create your views here.
def home(request):
    return render(request, "index.html")

@login_required
def orderform(request):
    form = NewCustomerForm(request.POST, request.FILES)
    form2 = CouponApplyForm(request.POST or None)
    if request.method == 'POST':
        print('success form is post')
        if form.is_valid() and form2.is_valid():
           
            # Now save the order to the database
            form.save()
            form2.save()


            
            messages.success(request, 'Order request submitted successfully.')
            
        else:
            messages.error(request, 'Invalid form submission.')
            print(form.errors.as_data())
            print(form2.errors.as_data())
            form = NewCustomerForm()
            form2 = CouponApplyForm()
 
    else:
        form = NewCustomerForm()
        form2 = CouponApplyForm()
        print('failed form is get')
    
    context = {
        'form': form,
        'form2': form2,
    }
    
    return render(request, "orderform.html", context=context)

def process_payment(request):
    request.session['order_id'] = '1'
    order_id = request.session.get('order_id', 1)
    print(f'my order id is {order_id}')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()


    # What you want the button to do.
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % Decimal(order.total_cost()).quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        
    }

    form=PayPalPaymentsForm(initial=paypal_dict)
    context={'form':form}
    print(context)
    return render(request, 'payments/process_payment.html', {'order': order, 'form': form})
    #return HttpResponse(f"Visit count:{request.session['visit']}")
    

def payment_done(request):
    return render(request, 'payments/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payments/payment_cancelled.html')

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
        #...
        #...

            cart.clear(request)

            request.session['order_id'] = o.id
            return redirect('process_payment')


    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', locals())



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Coupon
from .forms import CouponForm
from cart.cart import Cart
from suds.client import Client
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = CouponForm()
    context = {
        'form': form,
        'order': order,
    }
    return render(request, 'orders/order.html', context)


@login_required
def order_create(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)

    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'],
                                    price=item['price'], count=item['count'])
        
    
    return redirect('orders:order_detail', order.id)


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
description = "توضیحات پرداخت" 
mobile = '09123456789'  
amount = None
CallbackURL = 'http://localhost:8000/orders/verify/'


@login_required
def payment(request, order_id, price):
    global amount, o_id
    amount = price
    o_id = order_id
    result = client.service.PaymentRequest(
         MERCHANT, amount, description, request.user.email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

@login_required
def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(
            MERCHANT, request.GET['Authority'], amount)
        
        if result.Status == 100:
            cart = Cart(request)
            cart.clear()
            order = get_object_or_404(Order, id=o_id)
            order.paid = True
            order.save()
            messages.success(request, 'Paied {} success'.format(amount), 'success')
            return redirect('shop:home')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted' )
        else:
            return HttpResponse('Transaction failed')
    else:
        return HttpResponse('Transaction failed or canceled by user')

@require_POST
def coupon_apply(request, order_id):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, 
                                                        valid_to__gte=now, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'Copon not valid', 'danger')
            return redirect('orders:order_detail', order_id)

        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect('orders:order_detail', order.id)
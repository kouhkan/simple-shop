from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import AddCardForm


def detail(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }
    return render(request, 'cart/detail.html', context)

@require_POST
def add_card(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddCardForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                    count=cd['count'])
        messages.success(request, '{} add to cart'.format(product.name), 
        'success') 
        return redirect('cart:cart_detail')


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart:cart_detail')
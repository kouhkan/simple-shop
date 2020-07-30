from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import AddCardForm

# Create your views here.
def home(request, slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.filter(is_sub=False)

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    form = AddCardForm()

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'shop/product_detail.html', context)
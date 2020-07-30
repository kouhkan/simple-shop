from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.detail, name='cart_detail'),
    path('add/<int:product_id>', views.add_card, name='add_card'),
    path('remove/<int:product_id>', views.remove_cart, name='remove_cart'),
]

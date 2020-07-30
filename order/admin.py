from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderitemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'paid')
    list_filter = ('paid', )
    inlines = (OrderitemInline, )


@admin.register(Coupon)
class Coupon(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'active')
    list_filter = ('active', 'discount')
    search_fields = ('code', )
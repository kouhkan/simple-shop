from django.contrib import admin

from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name', )}

    actions = ('make_available', )

    def make_available(self, request, queryset):
        row = queryset.update(available=True)
        self.message_user(request, f'{row} updated')
    make_available.short_description = 'Make Available'
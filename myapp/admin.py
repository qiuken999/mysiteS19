from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Category, Client, Order

def add_stock(modeladmin, request, queryset):
    for product in queryset:
        product.stock = product.stock +50
        product.save()
    add_stock.short_description = 'Stock add 50'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    actions = [add_stock]

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)


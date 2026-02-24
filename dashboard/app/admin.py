from django.contrib import admin
from .models import Category, Product
from .models import Sale, SaleItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'quantity', 'created_at')
    fields = ('name', 'sku', 'category', 'purchase_price',
              'selling_price', 'quantity', 'minimum_stock', 'created_at')


admin.site.register(Category)
admin.site.register(Sale)
admin.site.register(SaleItem)
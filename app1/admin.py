from django.contrib import admin
from .models import Product, Order, LineItem, Coupon

# Register your models here.

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']

class LineItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'date_added', 'order']


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'email', 'date', 'paid', 'academic_level', 'type_of_service',
        'type_of_paper', 'subject_area', 'title', 'paper_format', 'number_of_pages',
        'currency', 'sources', 'powerpoint_slides', 'deadline', 'writer_category',
        'preferred_writers_id'
    ]

    

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(LineItem, LineItemAdmin)

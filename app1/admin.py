from django.contrib import admin
from .models import Product, Order, LineItem, Coupon, AdditionalMaterial

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

class AdditionalMaterialInline(admin.TabularInline):
    model = AdditionalMaterial
    extra = 1  # Number of empty forms to display

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'email', 'date', 'paid', 'academic_level', 'type_of_service',
        'type_of_paper', 'subject_area', 'title', 'paper_format', 'number_of_pages',
        'currency', 'sources', 'powerpoint_slides', 'deadline', 'writer_category',
        'preferred_writers_id', 'display_additional_material'
    ]
    inlines = [AdditionalMaterialInline]

    def display_additional_material(self, obj):
        # Display a count of additional materials
        return f'{obj.additional_materials.count()} files'
    display_additional_material.short_description = 'Additional Materials'

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(LineItem, LineItemAdmin)

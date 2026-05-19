from django.contrib import admin
from .models import Order, OrderItem, Coupon

# 1. This allows the Order Items to appear INSIDE the Order page
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # This makes the fields read-only so the owner doesn't accidentally change them
    readonly_fields = ('product_name', 'price', 'custom_details', 'custom_name', 'font', 'color')
    extra = 0 # Prevents empty rows from showing up
    can_delete = False # Prevents accidental deletion of items from an order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    
    # 2. Add the Inline here
    inlines = [OrderItemInline]
    
    # Optional: Make the money fields read-only to prevent tampering
    readonly_fields = ('subtotal', 'gst', 'total_amount', 'user', 'created_at')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active', 'created_at')

# If OrderItem was registered separately before, you can keep it or remove it
# admin.site.register(OrderItem)
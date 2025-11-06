from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]


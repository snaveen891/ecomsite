from django.contrib import admin

from .models import Order, OrderItem, CancellationRequest

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user' ,'first_name', 'last_name', 'email', 'amount', 'razorpay_payment_id', 'status']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

    def amount(self, obj):
        return obj.get_total_cost()


@admin.register(CancellationRequest)
class CancellationAdmin(admin.ModelAdmin):
    list_display = ['order', 'reason', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
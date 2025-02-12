from django.db import models
from store.models import Product
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    refunded = models.BooleanField(default=False)
    class Status(models.TextChoices):
        PENDING = "PE", "Pending"
        PROCESSING = "P", "Processing"
        SHIPPED = "S", "Shipped"
        DELIVERED = "D", "Delivered"
        CANCELLATION_REQUESTED = "CR", "Cancellation Requested"
        CANCELLED = "C", "Cancelled"
        FAILED = "F", "Failed"
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)
    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['created', 'updated']),
        ]
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(F"OrderItem {self.id} {self.product} x {self.quantity}")
    def get_cost(self):
        return self.price * self.quantity
    

class CancellationRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cancellations')
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class status(models.TextChoices):
        PENDING = "P", "Pending"
        APPROVED = "A", "Approved"
        REJECTED = "R", "Rejected"
    status = models.CharField(max_length=1, choices=status.choices, default=status.PENDING)
    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['created', 'updated']),
        ]
    def __str__(self):
        return f'Order {self.order.id} Cancellation'
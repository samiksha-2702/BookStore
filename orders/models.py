from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),          # Order placed but not processed
        ('Processing', 'Processing'),    # Being prepared
        ('Shipped', 'Shipped'),          # Dispatched
        ('Completed', 'Completed'),      # Delivered
        ('Cancelled', 'Cancelled'),      # Cancelled
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)  # <-- new field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} ({self.quantity})"
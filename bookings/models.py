from django.db import models
from django.contrib.auth.models import User
from services.models import ServiceProvider


class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_date = models.DateField()

    booking_time = models.TimeField()

    address = models.TextField()

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer.username} - {self.provider}"


class Review(models.Model):

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField()

    review = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('customer', 'provider')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.username} - {self.provider} - {self.rating}/5"


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('PhonePe', 'PhonePe'),
        ('Paytm', 'Paytm'),
        ('Google Pay', 'Google Pay'),
        ('UPI', 'UPI'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.customer.username} - ₹{self.amount} - {self.payment_status}"
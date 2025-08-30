from django.db import models

# Create your models here.
class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)  # Assuming a simple string for user, can be replaced with a User model
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.user}"
    
class Payment(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)  # e.g., 'Pending', 'Completed', 'Failed'

    def __str__(self):
        return f"Payment of {self.amount} for {self.booking.listing.title} on {self.payment_date}"
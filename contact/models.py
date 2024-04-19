from django.db import models


class ContactRequest(models.Model):
    """Model to store contact requests."""
    CATEGORY_CHOICES = [
        ('general', 'General Query'),
        ('update', 'Booking Update Request'),
        ('cancellation', 'Booking Cancellation'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        """Return a string representation of the contact request."""
        return f"{self.name} - {self.category}"

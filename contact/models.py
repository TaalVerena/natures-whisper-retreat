from django.db import models

# Create your models here.
class ContactRequest(models.Model):
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
        return f"{self.name} - {self.category}"
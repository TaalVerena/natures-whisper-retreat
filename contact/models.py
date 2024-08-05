from django.db import models
from django.contrib.auth.models import User


class ContactRequest(models.Model):
    """Model to store contact requests."""

    CATEGORY_CHOICES = [
        ("general", "General Query"),
        ("update", "Booking Update Request"),
        ("cancellation", "Booking Cancellation"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    lodge_reply = models.TextField(blank=True, null=True)

    def __str__(self):
        """Return a string representation of the contact request."""
        return f"{self.name} - {self.category}"

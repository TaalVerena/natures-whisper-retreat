from django.db import models
from django.conf import settings
from lodges.models import Lodge
from django.core.validators import MinValueValidator

class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lodge = models.ForeignKey("lodges.Lodge", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_nights = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )

    def __str__(self):
        return f"{self.lodge} reservation from {self.start_date} to {self.end_date}, Status: {self.status}"
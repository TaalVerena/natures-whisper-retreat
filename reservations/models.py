from django.db import models
from django.conf import settings
from lodges.models import Lodge


# Create your models here.
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lodge = models.ForeignKey('lodges.Lodge', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.IntegerField()

    def __str__(self):
        return f"{self.lodge} reservation from {self.start_date} to {self.end_date} for {self.guests}"
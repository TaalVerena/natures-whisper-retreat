from django.db import models
from cloudinary.models import CloudinaryField

class Lodge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    amenities = models.TextField()
    image = CloudinaryField('image')
    rate = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, help_text="Base rate per night")

    def __str__(self):
        return self.name
from django.db import models
from cloudinary.models import CloudinaryField

class Lodge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    amenities = models.TextField()
    image = CloudinaryField('image')
    amenityImage1 = CloudinaryField('amenity image 1', null=True)
    amenityImage2 = CloudinaryField('amenity image 2', null=True)
    sleeps = models.IntegerField(help_text="Number of guests the lodge sleeps")
    rate = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, help_text="Base rate per night")

    def __str__(self):
        return self.name
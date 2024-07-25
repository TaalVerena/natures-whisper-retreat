from django.db import models
from cloudinary.models import CloudinaryField


class Lodge(models.Model):
    """
    Model representing a lodge available for booking.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    amenities = models.TextField()
    image = CloudinaryField("image")
    amenityImage1 = CloudinaryField(
        "amenity image 1",
        null=True,
    )
    amenityImage2 = CloudinaryField(
        "amenity image 2",
        null=True,
    )
    sleeps = models.IntegerField()
    rate = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    def __str__(self):
        """
        String for representing the Lodge object (name).
        """
        return self.name

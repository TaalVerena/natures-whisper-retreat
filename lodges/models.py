from django.db import models
from cloudinary.models import CloudinaryField


class Lodge(models.Model):
    """
    Model representing a lodge available for booking.
    """
    name = models.CharField(max_length=200, help_text="The name of the lodge")
    description = models.TextField(
        help_text="A brief description of the lodge"
        )
    amenities = models.TextField(
        help_text="A list of amenities provided by the lodge"
        )
    image = CloudinaryField(
        'image', help_text="The main image of the lodge"
        )
    amenityImage1 = CloudinaryField(
        'amenity image 1',
        null=True,
        help_text="Optional additional image of lodge amenities"
        )
    amenityImage2 = CloudinaryField(
        'amenity image 2',
        null=True,
        help_text="Optional additional image of lodge amenities"
        )
    sleeps = models.IntegerField(
        help_text="Number of guests the lodge sleeps"
        )
    rate = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        help_text="Base rate per night"
        )

    def __str__(self):
        """
        String for representing the Lodge object (name).
        """
        return self.name

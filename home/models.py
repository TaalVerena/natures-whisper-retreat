from django.db import models
from cloudinary.models import CloudinaryField


class LodgeOverview(models.Model):
    """
    Model representing an overview of a lodge.

    This model contains basic information about a lodge,
    such as its name, description, and image.

    Attributes:
        name (CharField): The name of the lodge.
        description (TextField): A brief description of the lodge.
        image (CloudinaryField): The image associated with the lodge.
    """

    name = models.CharField(max_length=100, help_text="Enter the name of the lodge")
    description = models.TextField(
        max_length=400, help_text="Enter a brief description of the lodge"
    )
    image = CloudinaryField("image", help_text="Select an image for the lodge")

    class Meta:
        verbose_name = "Lodge overview"
        verbose_name_plural = "Lodge overviews"

    def __str__(self):
        """
        String representation of the LodgeOverview object.

        Returns:
            str: The name of the lodge.
        """
        return self.name

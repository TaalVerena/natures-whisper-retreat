from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Lodge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    amenities = models.TextField()
    image = CloudinaryField('image')

    def __str__(self):
        return self.name
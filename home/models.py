from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class LodgeOverview(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    image = CloudinaryField('image')

    class Meta:
        verbose_name = "Lodge overview"
        verbose_name_plural = 'Lodge overview'

    def __str__(self):
        return self.name
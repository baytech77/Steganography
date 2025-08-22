from django.db import models

# Create your models here.

from django.db import models

class EncodedImage(models.Model):
    cover_image = models.ImageField(upload_to='cover_images/')
    secret_message = models.TextField()
    password = models.CharField(blank=True, null=True)
    encoded_image = models.ImageField(upload_to='encoded_images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.cover_image.name} - EncodedImage {self.id}  "

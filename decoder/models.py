from django.db import models

# Create your models here.

class DecodedImage(models.Model):
    encoded_image = models.ImageField(upload_to='decoded_inputs/')
    decoded_message = models.TextField(blank=True, null=True)
    decoded_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.encoded_image.name} - EncodedImage {self.id}  "
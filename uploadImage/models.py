from django.db import models

from registration.models import RegisteredUsers

# Create your models here.

class ImageStorage(models.Model):
    # userdetails= models.ForeignKey(RegisteredUsers,on_delete=models.CASCADE)
    image= models.ImageField(upload_to='Assets/')

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "Image_storage_db"

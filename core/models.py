from django.db import models


# Create your models here.
class RasterImage(models.Model):
    name = models.CharField(max_length=50,unique=True)
    file =models.FileField(upload_to='image/')
    filename=models.CharField(max_length=50,null=True,blank=True)
    extension=models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return self.name
    # def save(self):
    #     fil
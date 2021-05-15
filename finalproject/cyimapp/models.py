from django.db import models

# Create your models here.
class foodTable(models.Model):
    fName = models.CharField(max_length = 20, null = False )
    #fFoodImage = models.ImageField(upload_to='image/food/', blank=False, null=True)
    fMenuImage = models.ImageField(upload_to='static/image/menu/', blank=True, null=True)
    fAddress = models.CharField(max_length = 255, blank = True, default='')
    fUrl = models.CharField(max_length = 255, null = False, default='' )
    fTag = models.CharField(max_length = 20, null = False, default='' )
    def __str__(self):
        return self.fName

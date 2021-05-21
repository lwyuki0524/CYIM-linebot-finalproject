from django.db import models

# Create your models here.
class foodTable(models.Model):
    fName = models.CharField(max_length = 20, null = False )
    fMenuImage = models.ImageField(upload_to='static/img/menu/', blank=True, null=True)
    fAddress = models.CharField(max_length = 255, blank = True, default='')
    fUrl = models.CharField(max_length = 255, null = False, default='' )
    fTag = models.CharField(max_length = 20, null = False, default='' )
    fLongitude = models.CharField(max_length = 20, null = False, default='' )
    fLatitude = models.CharField(max_length = 20, null = False, default='' )
    fStartTime  = models.TimeField(null=True ) 
    fEndTime = models.TimeField(null=True) 
    def __str__(self):
        return self.fName

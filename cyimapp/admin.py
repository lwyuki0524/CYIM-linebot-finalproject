from django.contrib import admin
from cyimapp.models import foodTable,UbikeData

# Register your models here.

class foodadmin(admin.ModelAdmin):
    list_display = ('id', 'fName', 'fMenuImage', 'fAddress','fUrl','fTag','fLongitude','fLatitude','fStartTime','fEndTime')#, 'fFoodImage'
    list_filter = ('fName','fTag')
    search_fields = ('fName',)
    ordering = ('id',)

class Ubikeadmin(admin.ModelAdmin):
    list_display = ('id', 'sno', 'sna', 'sbi','bemp')
    list_filter = ('sno','sna')
    search_fields = ('sna',)
    ordering = ('id',)

admin.site.register(foodTable, foodadmin)
admin.site.register(UbikeData, Ubikeadmin)

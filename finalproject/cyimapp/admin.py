from django.contrib import admin
from cyimapp.models import foodTable

# Register your models here.

class foodadmin(admin.ModelAdmin):
    list_display = ('id', 'fName', 'fMenuImage', 'fAddress','fUrl','fTag')#, 'fFoodImage'
    list_filter = ('fName','fTag')
    search_fields = ('fName',)
    ordering = ('id',)

admin.site.register(foodTable, foodadmin)

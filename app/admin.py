from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Main_Data_Upload)
admin.site.register(PhoneNumber)
admin.site.register(CsvFile)
admin.site.register(Train_Type)


from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import *

admin.site.register(Food)
admin.site.register(Symptom)
admin.site.register(Medicine)
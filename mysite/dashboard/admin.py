from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Food, Symptom

admin.site.register(Food)
admin.site.register(Symptom)

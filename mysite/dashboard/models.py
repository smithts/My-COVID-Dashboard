from django.db import models

# Create your models here.

from django.db import models
from django.forms import ModelForm
from .utils import  SEVERITY

class Food_Mode(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Food_Contact(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Food(models.Model):

    log_date = models.DateTimeField('Date')
    restaurant = models.CharField(max_length=200)
    dishes = models.CharField(max_length=200)
    mode = models.ForeignKey(Food_Mode, on_delete=models.CASCADE)
    contact = models.ForeignKey(Food_Contact, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant + " - " +self.dishes

class FoodForm(ModelForm):
    class Meta:
        model=Food
        fields=[ 'log_date', 'restaurant', 'dishes', 'mode', 'contact']

class SymptomType(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Symptom(models.Model):
    date = models.DateTimeField('Date')
    type = models.ForeignKey(SymptomType, on_delete=models.CASCADE)
    severity = models.IntegerField(choices=SEVERITY, default=1)
    notes = models.CharField(max_length=200, null=True)

class SymptomForm(ModelForm):
    class Meta:
        model=Symptom
        fields=['date', 'type', 'severity', 'notes']




# class Choice(models.Model):
#     question = models.ForeignKey(Food, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
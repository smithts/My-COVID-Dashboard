from django.db import models

# Create your models here.

from django.db import models
from django.forms import ModelForm
from .utils import SEVERITY


# Food
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
    contactless = models.BooleanField(default=True)

    def __str__(self):
        return self.restaurant + " - " + self.dishes


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['log_date', 'restaurant', 'dishes', 'mode', 'contactless']


# Medicine
class Medicine(models.Model):
    log_date = models.DateTimeField('date published')
    type = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)

    def __str__(self):
        return self.quantity + " of " + self.type


class MedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ['log_date', 'type', 'quantity', 'purpose']


# Symptom
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
        model = Symptom
        fields = ['date', 'type', 'severity', 'notes']


# Friend
class Friend(models.Model):
    log_date = models.DateTimeField('date published')
    friend = models.CharField(max_length=100)
    duration = models.CharField(max_length=6)
    indoor = models.BooleanField(default=False)
    masked = models.BooleanField(default=True)
    distanced = models.BooleanField(default=True)

    def __str__(self):
        return "Interaction with " + self.friend + " for " + self.duration + "minutes."


class FriendForm(ModelForm):
    class Meta:
        model = Friend
        fields = ['log_date', 'friend', 'duration', 'indoor', 'masked', 'distanced']


# Doctor
class Doctor(models.Model):
    log_date = models.DateTimeField('date published')
    doctor = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    outcome = models.CharField(max_length=200)

    def __str__(self):
        return "Visit to " + self.doctor + " for " + self.purpose


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['log_date', 'doctor', 'specialty', 'purpose', 'outcome']


# Trip
class Trip(models.Model):
    log_date = models.DateTimeField('date published')
    destination = models.CharField(max_length=100)
    travel_mode = models.CharField(max_length=100)
    masked = models.BooleanField(default=True)

    def __str__(self):
        return "Travelled to " + self.destination + " in a " + self.travel_mode + "."


class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ['log_date', 'destination', 'travel_mode', 'masked']

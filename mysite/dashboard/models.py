from django.db import models

# Create your models here.

from django.db import models
from django.forms import ModelForm
from django import forms

SEVERITY= [tuple([x,x]) for x in range(1,6)]

class DateInput(forms.DateInput):
    input_type = 'date'

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
    MODE_CHOICES = (
        ('PU', 'Pick-up'),
        ('DV', 'Delivery'),
    )

    log_date = models.DateField('Date')
    restaurant = models.CharField(max_length=200)
    dishes = models.CharField(max_length=200)
    mode = models.CharField(max_length=2, choices=MODE_CHOICES)
    contactless = models.BooleanField(default=True)

    def __str__(self):
        return self.restaurant + " - " + self.dishes


class FoodForm(ModelForm):
    class Meta:
        widgets = {'log_date': DateInput()}
        model = Food
        fields = ['log_date', 'restaurant', 'dishes', 'mode', 'contactless']


# Medicine
class Medicine(models.Model):
    log_date = models.DateField('date published')
    type = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)

    def __str__(self):
        return self.quantity + " of " + self.type


class MedicineForm(ModelForm):
    class Meta:
        widgets = {'log_date': DateInput()}
        model = Medicine
        fields = ['log_date', 'type', 'quantity', 'purpose']


# Symptom
class SymptomType(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Symptom(models.Model):
    SYMPTOM_CHOICES = (
        ('FV', 'Fever'),
        ('CL', 'Chills'),
        ('CH', 'Cough'),
        ('DB', 'Difficulty Breathing'),
        ('ST', 'Sore Throat'),
        ('MA', 'Muscle Aches'),
        ("HA", "Headache"),
        ('DH', 'Diarrhea'),
        ('SF', 'Severe Fatigue'),
        ('NC', 'Nasal Congestion'),
        ('LT', 'New Loss of Taste'),
        ('LS', 'New Loss of Smell'),
        ('OT', 'Other')
    )

    log_date = models.DateField('Date')
    #type = models.ForeignKey(SymptomType, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=SYMPTOM_CHOICES)
    severity = models.IntegerField(choices=SEVERITY, default=1)
    notes = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.type + " of severity " + str(self.severity) + " on " + str(self.log_date)



class SymptomForm(ModelForm):
    class Meta:
        widgets = {'log_date': DateInput()}
        model = Symptom
        fields = ['log_date', 'type', 'severity', 'notes']


# Friend
class Friend(models.Model):
    log_date = models.DateField('date published')
    friend = models.CharField(max_length=100)
    duration = models.IntegerField()
    indoor = models.BooleanField(default=False)
    masked = models.BooleanField(default=True)
    distanced = models.BooleanField(default=True)

    def __str__(self):
        return "Interaction with " + self.friend + " for " + str(self.duration) + " minutes."

class FriendForm(ModelForm):
    class Meta:
        widgets = {'log_date': DateInput()}
        model = Friend
        fields = ['log_date', 'friend', 'duration', 'indoor', 'masked', 'distanced']


# Doctor
class Doctor(models.Model):
    log_date = models.DateField('date published')
    doctor = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    outcome = models.CharField(max_length=200)

    def __str__(self):
        return "Visit to " + self.doctor + " for " + self.purpose


class DoctorForm(ModelForm):
    class Meta:
        widgets = {'log_date': DateInput()}
        model = Doctor
        fields = ['log_date', 'doctor', 'specialty', 'purpose', 'outcome']


# Trip
class Trip(models.Model):
    log_date = models.DateField('date published')
    destination = models.CharField(max_length=100)
    travel_mode = models.CharField(max_length=100)
    masked = models.BooleanField(default=True)

    def __str__(self):
        return "Travelled to " + self.destination + " in a " + self.travel_mode + "."


class TripForm(ModelForm):
    class Meta:
        widgets = {'log_date': DateInput()}
        model = Trip
        fields = ['log_date', 'destination', 'travel_mode', 'masked']

# Sync Device
class Device(models.Model):
    DEVICE_CHOICES = (
        ('AW', 'Apple Watch'),
        ('FB', 'Fitbit'),
        ('IP','iPhone'),
        ('AD','Android'),
    )
    device = models.CharField(max_length=2, choices=DEVICE_CHOICES)
    date_added = models.DateField('date published')

    def __str__(self):
        return self.device + " added on " + self.date_added + "."

class DeviceForm(ModelForm):
    class Meta:
        widgets = {'date_added': DateInput()}
        model = Device
        fields = ['device', 'date_added']

# Sync Health Data
class HealthData(models.Model):

    device = models.CharField(max_length=100)
    log_date = models.DateField('date published')
    activity = models.CharField(max_length=100)

    def __str__(self):
        return self.activity + " logged on " + self.log_date + "."

class HealthDataForm(ModelForm):
    class Meta:
        widgets = {'log_date': DateInput()}
        model = HealthData
        fields = ['log_date', 'device', 'activity']

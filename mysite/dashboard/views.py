from django.http import HttpResponse

from .models import *


from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from datetime import timedelta
from django.utils import timezone
from .utils import get_risk
import logging

logger = logging.getLogger(__name__)

#indicates a log_date decending ordering
log_order = '-log_date'

def index(request):

    #get all logs within the past 2 weeks
    two_weeks_ago = timezone.now().date() - timedelta(days=14)

    #all food logs within 2 weeks
    food = Food.objects.filter(log_date__gte=two_weeks_ago)
    trips = Trip.objects.filter(log_date__gte=two_weeks_ago)
    symptoms = Symptom.objects.filter(log_date__gte=two_weeks_ago)
    friends = Friend.objects.filter(log_date__gte=two_weeks_ago)

    for instance in food:
        if (instance.contactless == False):
            logger.error(str(instance.log_date) + ": " + instance.restaurant)

    #all food logs that had pickups with contact
    #food_contact = Food_Contact.objects.filter(title__exact="No").get()
    #food = food_contact.food_set.filter(log_date__gte=two_weeks_ago)

    risk = get_risk([food])

    context = {
        'risk': risk
    }

    return render(request, 'index.html', context)

# Food
def view_food(request):
    headers = ['Date', 'Restaurant', 'Dishes', 'Type', 'Contactless', '']

    context = {
        'food': Food.objects.all().order_by(log_order),
        'headers':headers
    }
    return render(request, 'food/index.html', context)

def add_food(request):
    form = FoodForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/food/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'food/add.html', context)

def delete_food(request, id):
    Food.objects.filter(id=id).delete()
    return view_food(request)

def success_food(request):
    return render(request, 'food/success.html')

# Symptoms
def add_symptom(request):
    form = SymptomForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/symptom/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'symptom/add.html', context)

def view_symptom(request):
    context = {
        'symptoms':Symptom.objects.all().order_by(log_order),
        'headers': ['Date', 'Type', 'Severity', 'Notes', '']
    }
    return render(request, 'symptom/index.html', context)

def delete_symptom(request, id):
    Symptom.objects.filter(id=id).delete()
    return view_symptom(request)

def success_symptom(request):
    return render(request, 'symptom/success.html')


# Medicine
def view_medicine(request):
    headers = ['Date', 'Type', 'Quantity', 'Purpose', '']

    context = {
        'medicine': Medicine.objects.all().order_by(log_order),
        'headers': headers
    }

    return render(request, 'medicine/index.html', context)

def add_medicine(request):
    form = MedicineForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/medicine/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'medicine/add.html', context)

def delete_medicine(request, id):
    Medicine.objects.filter(id=id).delete()
    return view_medicine(request)

def success_medicine(request):
    return render(request, 'medicine/success.html')

# Doctor
def view_doctor(request):
    headers = ['Date', 'Doctor', 'Specialty', 'Purpose', 'Outcome', '']

    context = {
        'doctor': Doctor.objects.all().order_by(log_order),
        'headers': headers
    }

    return render(request, 'doctor/index.html', context)

def add_doctor(request):
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/doctor/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'doctor/add.html', context)

def delete_doctor(request, id):
    Doctor.objects.filter(id=id).delete()
    return view_doctor(request)

def success_doctor(request):
    return render(request, 'doctor/success.html')

# Friend
def view_friend(request):
    headers = ['Date', 'Friend', 'Duration (Minutes)', 'Indoor', 'Masked', 'Distanced', '']

    context = {
        'friend': Friend.objects.all().order_by(log_order),
        'headers': headers
    }

    return render(request, 'friend/index.html', context)

def add_friend(request):
    form = FriendForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/friend/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'friend/add.html', context)

def delete_friend(request, id):
    Friend.objects.filter(id=id).delete()
    return view_friend(request)

def success_friend(request):
    return render(request, 'friend/success.html')

# Trip
def view_trip(request):
    headers = ['Date', 'Location', 'Travel Mode', 'Masked', '']

    context = {
        'trip': Trip.objects.all().order_by(log_order),
        'headers': headers
    }

    return render(request, 'trip/index.html', context)

def add_trip(request):
    form = TripForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/trip/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'trip/add.html', context)

def delete_trip(request, id):
    Trip.objects.filter(id=id).delete()
    return view_trip(request)

def success_trip(request):
    return render(request, 'trip/success.html')


# Sync Device
'''
def view_device(request):
    headers = ['Device', 'Date Added', '']

    context = {
        'device': Device.objects.all(),
        'headers': headers
    }

    return render(request, 'sync/index.html', context)
'''
# Sync Device
'''
def view_healthData(request):
    headers = ['Date', 'From', 'Activity', '']

    context = {
        'data': HealthData.objects.all(),
        'headers': headers
    }

    return render(request, 'sync/index.html', context)
'''
def view_sync(request):
    deviceHeaders = ['Device', 'Date Added', '']
    healthHeaders = ['Date', 'From', 'Activity', '']

    context = {
        'device': Device.objects.all().order_by('-date_added'),
        'deviceHeaders': deviceHeaders,
        'data': HealthData.objects.all().order_by(log_order),
        'healthHeaders': healthHeaders
    }

    return render(request, 'sync/index.html', context)

def add_device(request):
    form = DeviceForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/sync/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'sync/add.html', context)

def delete_device(request, id):
    Device.objects.filter(id=id).delete()
    return view_sync(request)

def success_sync(request):
    return render(request, 'sync/success.html')





def success(request):
    return render(request, 'save/success.html')

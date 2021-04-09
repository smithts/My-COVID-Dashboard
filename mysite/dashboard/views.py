from django.http import HttpResponse

from .models import *


from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from datetime import timedelta
from django.utils import timezone
from .utils import get_risk

def index(request):

    #get all logs within the past 2 weeks
    two_weeks_ago = timezone.now().date() - timedelta(days=14)

    #all food logs within 2 weeks
    food = Food.objects.filter(log_date__gte=two_weeks_ago)

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
        'food': Food.objects.all(),
        'headers':headers
    }
    return render(request, 'food/index.html', context)

def add_food(request):
    form = FoodForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'food/add.html', context)

def delete_food(request, id):
    Food.objects.filter(id=id).delete()
    return view_food(request)

# Symptoms
def add_symptom(request):
    form = SymptomForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/symptom')
        return response

    context = {
        'form': form,
    }
    return render(request, 'symptom/add.html', context)

def view_symptom(request):
    context = {
        'symptoms':Symptom.objects.all(),
        'headers': ['Date', 'Type', 'Severity', 'Notes', '']
    }
    return render(request, 'symptom/index.html', context)

def delete_symptom(request, id):
    Symptom.objects.filter(id=id).delete()
    return view_symptom(request)

# Medicine
def view_medicine(request):
    headers = ['Date', 'Type', 'Quantity', 'Purpose', '']

    context = {
        'medicine': Medicine.objects.all(),
        'headers': headers
    }

    return render(request, 'medicine/index.html', context)

def add_medicine(request):
    form = MedicineForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'medicine/add.html', context)

def delete_medicine(request, id):
    Medicine.objects.filter(id=id).delete()
    return view_medicine(request)
'''
def detail_medicine(request, id):

    context = {
        'medicine': Medicine.objects.get(pk=id)
    }
    return render(request, 'medicine/detail.html', context)
'''

# Doctor
def view_doctor(request):
    headers = ['Date', 'Doctor', 'Specialty', 'Purpose', 'Outcome', '']

    context = {
        'doctor': Doctor.objects.all(),
        'headers': headers
    }

    return render(request, 'doctor/index.html', context)

def add_doctor(request):
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'doctor/add.html', context)

def delete_doctor(request, id):
    Doctor.objects.filter(id=id).delete()
    return view_doctor(request)



# Friend
def view_friend(request):
    headers = ['Date', 'Friend', 'Duration (Minutes)', 'Indoor', 'Masked', 'Distanced', '']

    context = {
        'friend': Friend.objects.all(),
        'headers': headers
    }

    return render(request, 'friend/index.html', context)

def add_friend(request):
    form = FriendForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'friend/add.html', context)

def delete_friend(request, id):
    Friend.objects.filter(id=id).delete()
    return view_friend(request)

# Trip
def view_trip(request):
    headers = ['Date', 'Location', 'Travel Mode', 'Masked', '']

    context = {
        'trip': Trip.objects.all(),
        'headers': headers
    }

    return render(request, 'trip/index.html', context)

def add_trip(request):
    form = TripForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/success')
        return response

    context = {
        'form': form,
    }
    return render(request, 'trip/add.html', context)

def delete_trip(request, id):
    Trip.objects.filter(id=id).delete()
    return view_trip(request)


def success(request):
    return render(request, 'save/success.html')

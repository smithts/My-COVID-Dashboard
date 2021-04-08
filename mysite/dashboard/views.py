from django.http import HttpResponse

from .models import Food, Food_Contact, FoodForm, Medicine, MedicineForm

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

def detail_food(request, id):

    context = {
        'food': Food.objects.get(pk=id),
    }
    return render(request, 'food/detail.html', context)

def success(request):
    return render(request, 'save/success.html')


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

def detail_medicine(request, id):

    context = {
        'medicine': Medicine.objects.get(pk=id)
    }
    return render(request, 'medicine/detail.html', context)

def view_doctor(request):
    return None

def view_symptom(request):
    return None

def view_trip(request):
    return None
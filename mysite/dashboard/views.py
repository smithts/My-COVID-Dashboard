from django.http import HttpResponse

from .models import Food, FoodForm

from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic



def index(request):
    return HttpResponse("COVID RISK HIGH.")

def view(request):

    headers = ['Date', 'Restaurant', 'Dishes', 'Type', 'No Contact']

    context = {
        'food': Food.objects.all(),
        'headers':headers
    }
    return render(request, 'food/index.html', context)

def add(request):
    form = FoodForm(request.POST or None)
    if form.is_valid():
        form.save()
        response = redirect('/dashboard/food')
        return response

    context = {
        'form': form,
    }
    return render(request, 'food/add.html', context)

def detail(request, id):

    context = {
        'food': Food.objects.get(pk=id),
    }
    return render(request, 'food/detail.html', context)
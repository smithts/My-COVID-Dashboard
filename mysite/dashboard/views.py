from django.http import HttpResponse

from .models import Food, FoodForm

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

    food = Food.objects.filter(log_date__gte=two_weeks_ago)

    risk = get_risk([food])

    context = {
        'risk': risk
    }
    return render(request, 'index.html', context)


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
        response = redirect('/dashboard/success')
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

def success(request):
    return render(request, 'save/success.html')
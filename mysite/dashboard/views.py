from django.http import HttpResponse

from .models import Food
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'food/index.html'
    context_object_name = 'food'

    def get_queryset(self):
        """Return the last five published questions."""
        return Food.objects.all()[:5]

class DetailView(generic.DetailView):
    model = Food
    template_name = 'food/detail.html'

def index(request):
    return HttpResponse("COVID RISK HIGH.")

def add(request):
    return HttpResponse("ADD FOOD")


def detail(request, food_id):

    context = {
        'food': Food.objects.all(),
    }
    return render(request, 'food/index.html', context)
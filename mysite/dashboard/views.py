from django.http import HttpResponse

from .models import *
from django.shortcuts import render, redirect
from .utils import calculate_risk
import logging
import datetime
import random

logger = logging.getLogger(__name__)

#indicates a log_date decending ordering
log_order = '-log_date'

def index(request):
    risk = calculate_risk()

    context = {
        'risk': risk
    }

    return render(request, 'index.html', context)

# Food
def view_food(request):
    headers = ['Date', 'Restaurant', 'Dishes', 'Mode', 'Contactless', '']

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
        'symptoms': Symptom.objects.all().order_by(log_order),
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
    headers = ['Date', 'Location', 'Travel Mode', 'Duration (Days)', 'Masked', '']

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

def view_sync(request):
    deviceHeaders = ['Device', 'Date Added', '']
    healthHeaders = ['Date', 'From', 'Activity Log', 'Daily Step Count', '']

    data = []
    deviceList = Device.objects.all()
    if deviceList:
        d = deviceList[0]
        controller = device_controllers[d.device]
        data = controller.get_data()

    context = {
        'device': Device.objects.all().order_by('-date_added'),
        'deviceHeaders': deviceHeaders,
        'data': data,
        'healthHeaders': healthHeaders
    }

    return render(request, 'sync/index.html', context)

def add_device(request):
    form = DeviceForm(request.POST or None)
    if form.is_valid():
        # Retrieve device type from form request. If a device has already been synced, do nothing.
        user_device = form.cleaned_data.get('device')
        if not Device.objects.filter(device=user_device).exists() and len(Device.objects.all())==0:
            #iphone = iphone_controller()

            controller = device_controllers[user_device]

            user = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            if controller.test_credentials(user, pwd):
                form.save()
                response = redirect('/dashboard/sync/success')
            else:
                response = redirect('/dashboard/sync/failure_sync_access')

        else:
            response = redirect('/dashboard/sync/device_already_synced')
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

def failure_sync(request):
    context = {
        'error':'DEVICE HAS ALREADY BEEN SYNCED'
    }
    return render(request, 'sync/device_error.html', context)

def failure_sync_access(request):
    context = {
        'error':'DEVICE LOGIN CREDENTIALS INVALID'
    }
    return render(request, 'sync/device_error.html', context)

'''
def success(request):
    return render(request, 'save/success.html', context)
'''


class health_device_api_controller:
    def __init__(self, username="",password="", api_url="", name=""):
        self.username =username
        self.password=password
        self.api_url = api_url
        self.name = name

    def get_data(self):
        #mimic api request for health device api
        activities = [
            {'log_date': datetime.date.today(), 'device': self.name, 'activity': 'Run, 3.43 Miles, 365 Calories', 'step_count': random.randrange(12000, 25000)},
            {'log_date': datetime.date.today() - datetime.timedelta(days=1), 'device':self.name, 'activity': 'Bike Ride, 12.22 miles, 1573 Calories', 'step_count': random.randrange(12000, 25000)},
            {'log_date': datetime.date.today() - datetime.timedelta(days=2), 'device': self.name, 'activity': '-', 'step_count': random.randrange(12000, 25000)},
            {'log_date': datetime.date.today() - datetime.timedelta(days=3), 'device': self.name, 'activity': 'Run, 2.76 Miles, 297 Calories', 'step_count': random.randrange(12000, 25000)},
            {'log_date': datetime.date.today() - datetime.timedelta(days=4), 'device': self.name, 'activity': 'Bike Ride, 9.89 miles, 1224 Calories', 'step_count':random.randrange(12000, 25000)},
            {'log_date': datetime.date.today() - datetime.timedelta(days=5), 'device': self.name, 'activity': '-', 'step_count': random.randrange(12000, 25000)},
            {'log_date': datetime.date.today() - datetime.timedelta(days=6), 'device': self.name, 'activity': 'Bike Ride, 15.04 miles, 1880 Calories', 'step_count':random.randrange(12000, 25000)}
        ]
        return activities


    def test_credentials(self, username, password):
        if username and password:
            self.username=username
            self.password=password
            return True

class iphone_controller(health_device_api_controller):
    def __init__(self):
        api_url="http://api.icloud.com"
        name = "iPhone"
        super().__init__(api_url=api_url, name=name)

class android_controller(health_device_api_controller):
    def __init__(self):
        api_url = "http://api.android.com"
        name = "Android"
        super().__init__(api_url=api_url, name=name)

class fitbit_controller(health_device_api_controller):
    def __init__(self):
        api_url = "http://api.icloud.watch.com"
        name = "FitBit"
        super().__init__(api_url=api_url, name=name)

class apple_watch_controller(health_device_api_controller):
    def __init__(self):
        api_url = "http://api.fitbit.com"
        name = "Apple Watch"
        super().__init__(api_url=api_url, name=name)

device_controllers = {'IP':iphone_controller(), 'FB':fitbit_controller(), 'AW':apple_watch_controller(), 'AD':android_controller()}

from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # ex: /dashboard/
    path('', views.index, name='index'),

    #food
    path('food/', views.view_food, name='food_view'),
    path('food/add', views.add_food, name='add_food'),
    path('food/delete/<int:id>/', views.delete_food, name='delete_food'),
    path('food/success', views.success_food, name='success_food'),

    #friend
    path('friend/', views.view_friend, name='friend_view'),
    path('friend/add', views.add_friend, name='add_friend'),
    path('friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),
    path('friend/success', views.success_friend, name='success_friend'),

    #doctor
    path('doctor/', views.view_doctor, name='doctor_view'),
    path('doctor/add', views.add_doctor, name='add_doctor'),
    path('doctor/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('doctor/success', views.success_doctor, name='success_doctor'),

    #medicine
    path('medicine/', views.view_medicine, name="medicine_view"),
    path('medicine/add', views.add_medicine, name="add_medicine"),
    path('medicine/delete/<int:id>/', views.delete_medicine, name='delete_medicine'),
    path('medicine/success', views.success_medicine, name='success_medicine'),

    #symptom
    path('symptom/', views.view_symptom, name="symptom_view"),
    path('symptom/add', views.add_symptom, name="add_symptom"),
    path('symptom/delete/<int:id>/', views.delete_symptom, name="delete_symptom"),
    path('symptom/success', views.success_symptom, name='success_symptom'),

    #trip
    path('trip/', views.view_trip, name='trip_view'),
    path('trip/add', views.add_trip, name='add_trip'),
    path('trip/delete/<int:id>/', views.delete_trip, name='delete_trip'),
    path('trip/success', views.success_trip, name='success_trip'),

    #sync
    path('sync/', views.view_sync, name='view_sync'),
    path('sync/add', views.add_device, name='add_device'),
    path('sync/delete/<int:id>/', views.delete_device, name='delete_device'),
    path('sync/success', views.success_sync, name='success_sync'),

    #path('success', views.success, name='success')


]


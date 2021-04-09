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

    #friend
    path('friend/', views.view_friend, name='friend_view'),
    path('friend/add', views.add_friend, name='add_friend'),
    path('friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),

    #doctor
    path('doctor/', views.view_doctor, name='doctor_view'),
    path('doctor/add', views.add_doctor, name='add_doctor'),
    path('doctor/delete/<int:id>/', views.delete_friend, name='delete_doctor'),

    #medicine
    path('medicine/', views.view_medicine, name="medicine_view"),
    path('medicine/add', views.add_medicine, name="add_medicine"),
    path('medicine/delete/<int:id>/', views.delete_medicine, name='delete_medicine'),

    #symptom
    path('symptom/', views.view_symptom, name="view_symptom"),
    path('symptom/add', views.add_symptom, name="add_symptom"),
    path('symptom/delete/<int:id>/', views.delete_symptom, name="delete_symptom"),

    #trip
    path('trip/', views.view_trip, name='view_trip'),
    path('trip/add', views.add_trip, name='add_trip'),
    path('trip/delete/<int:id>/', views.delete_trip, name='delete_trip'),

    path('success', views.success, name='success')

]


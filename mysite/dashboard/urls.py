from django.urls import path, re_path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # ex: /dashboard/
    path('', views.index, name='index'),

    #food
    path('food/', views.view_food, name='food_view'),
    path('food/add', views.add_food, name='add_food'),
    path('food/delete/<int:id>/', views.delete_food, name='delete_food'),
    path('food/<int:id>/', views.detail_food, name='detail_food'),

    #medicine
    path('medicine/', views.view_medicine, name="medicine_view"),
    path('medicine/add', views.add_medicine, name="add_medicine"),
    path('medicine/delete/<int:id>/', views.delete_medicine, name='delete_medicine'),
    path('medicine/<int:id>/', views.detail_medicine, name="detail_medicine"),



    path('success', views.success, name='success')

]


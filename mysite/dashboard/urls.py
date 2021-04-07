from django.urls import path, re_path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # ex: /dashboard/
    path('', views.index, name='index'),
    # ex: /food/
    path('food/', views.view_food, name='food_view'),
    # ex: /food/5/
    path('food/<int:id>/', views.detail_food, name='detail'),
    # ex: /food/add/
    path('food/add', views.add_food, name='add'),
    path('success', views.success, name='success')
    #path('medicines/', views.view_medicine, name="medicine_view")
]


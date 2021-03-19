from django.urls import path, re_path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # ex: /dashboard/
    path('', views.index, name='index'),
    # ex: /food/
    path('food/', views.view, name='view'),
    # ex: /food/5/
    path('food/<int:id>/', views.detail, name='detail'),
    # ex: /food/add/
    path('food/add', views.add, name='add'),
    path('success', views.success, name='success')
]


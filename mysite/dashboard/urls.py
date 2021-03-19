from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # ex: /dashboard/
    path('', views.index, name='index'),
    # ex: /food/
    path('food/', views.IndexView.as_view(), name='view'),
    # ex: /food/5/
    #path('food/<int:pk>/', views.detail, name='detail'),
    path('food/<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /food/add/
    path('food/add', views.add, name='add'),

]


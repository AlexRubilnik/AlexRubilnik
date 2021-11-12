from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Furnace_1_info/', views.Furnace_1_info, name='Furnace_1_info'),
    path('Furnace_2_info/', views.Furnace_2_info, name='Furnace_2_info'),
]   
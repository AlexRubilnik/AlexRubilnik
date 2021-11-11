from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Furnace_1_power/', views.Furnace_1_power, name='Furnace_1_power'),
]    
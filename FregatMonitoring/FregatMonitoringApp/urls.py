from django.urls import path

from . import views

app_name = 'FregatMonitoringApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('ErrorMessage/', views.error_message, name='ErrorMessage'),
    path('Furnace_1_info/', views.Furnace_1_info, name='Furnace_1_info'),
    path('Furnace_2_info/', views.Furnace_2_info, name='Furnace_2_info'),
    path('Automelts_info/<int:meltID_1>/', views.AutoMeltTypes_info, name='Automelts_info'),
    path('AutoMeltsSaveSettings/<int:meltID_1>/<int:meltID_2>/', views.AutoMeltsSaveSettings, name='AutoMeltsSaveSettings'),
    path('AutoMeltsSetPoints/', views.AutoMelts_SetPoints, name='AutoMeltsSetPoints')
]   
from django.urls import path

from . import views

app_name = 'FregatMonitoringApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('ErrorMessage/', views.error_message, name='ErrorMessage'),
    path('SorryPage/', views.sorry_page, name='SorryPage'),
    path('Furnace_1_info/', views.Furnace_1_info, name='Furnace_1_info'),
    path('Furnace_2_info/', views.Furnace_2_info, name='Furnace_2_info'),
    path('Automelts_info/<int:meltID_1>/', views.AutoMeltTypes_info, name='Automelts_info'),
    path('AutoMeltsSaveSettings/<int:meltID_1>/<int:meltID_2>/', views.AutoMeltsSaveSettings, name='AutoMeltsSaveSettings'),
    path('AutoMeltsSetPoints/', views.AutoMelts_SetPoints, name='AutoMeltsSetPoints'),
    path('AutoMeltsSaveSetpoints/<int:furnace_num>/', views.AutoMeltsSaveSetpoints, name='AutoMeltsSaveSetpoints'),
    path('Furnace_info_s/<int:SignalIndex>/', views.Furnace_info_s, name='Furnace_info_s'),
    path('Furnace_info_a/<int:FurnaceNo>/', views.Furnace_info_a, name='Furnace_info_a')
]   
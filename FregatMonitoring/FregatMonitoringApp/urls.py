from unicodedata import name
from django.urls import path

from . import views

app_name = 'FregatMonitoringApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('ErrorMessage/', views.error_message, name='error_message'),
    path('SorryPage/', views.sorry_page, name='sorry_page'),
    path('Furnace_1_info/', views.furnace_1_info, name='furnace_1_info'),
    path('Furnace_2_info/', views.furnace_2_info, name='furnace_2_info'),
    path('FurnaceBaseTrends/<int:furnace_no>/', views.furnace_base_trends, name='furnace_base_trends'),
    path('FurnaceErrorsLog/<int:furnace_no>/', views.furnace_errors_log, name='furnace_errors_log'),
    path('FurnaceErrorsLogData/<int:furnace_no>/', views.furnace_errors_log_data, name='furnace_errors_log_data'),
    path('FurnaceBaseTrendsData/<int:furnace_no>/', views.furnace_base_trends_data, name='furnace_base_trends_data'),
    path('Automelts_info/<int:melt_id_1>/', views.auto_melts_types_info, name='auto_melts_types_info'),
    path('auto_melts_log/', views.auto_melts_log, name='auto_melts_log'),
    path('auto_melts_log_data/', views.auto_melts_log_data, name='auto_melts_log_data'),
    path('AutoMeltsSaveSettings/<int:melt_id_1>/<int:melt_id_2>/', views.auto_melts_save_settings, name='auto_melts_save_settings'),
    path('AutoMeltsSetPoints/', views.auto_melts_setpoints, name='auto_melts_setpoints'),
    path('AutoMeltsSetPoints/<int:furnace_num>/', views.auto_melts_save_setpoints, name='auto_melts_save_setpoints'),
    path('AutoMeltsAddSubstep/<str:melt_type>/<int:melt_step>/', views.auto_melts_add_substep, name='auto_melts_add_substep'),
    path('AutoMeltsDelSubstep/<str:melt_type>/<int:melt_step>/<int:melt_substep>/', views.auto_melts_del_substep, name='auto_melts_del_substep'),
    path('Furnace_info_s/<int:signal_index>/', views.furnace_info_s, name='furnace_info_s'),
    path('Furnace_info_a/<int:furnace_no>/', views.furnace_info_a, name='furnace_info_a'),
    path('ReportsPage/', views.reports_page, name='reports_page'),
    path('GasesUsage/<str:report_type>/', views.gases_usage_report, name='gases_usage_report'),
    path('getGasesUsageData_daily/', views.get_gases_usage_data_daily, name='get_gases_usage_data_daily'),
    path('getGasesUsageData_hourly/', views.get_gases_usage_data_hourly, name='get_gases_usage_data_hourly'),
    path('bottling_page/', views.bottling_page, name='bottling_page'),
    path('bottling_page_data/', views.bottling_page_data, name='bottling_page_data'),
    path('current_bottling_page/', views.current_bottling_page, name='current_bottling_page'),
    path('bottling_journal_data/', views.bottling_journal_data, name='bottling_journal_data'),
]   
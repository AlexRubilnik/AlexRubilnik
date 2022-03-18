from ast import Str
from calendar import month
from datetime import datetime, timedelta, date
import itertools
from multiprocessing import context 

from django.db.models.query_utils import subclasses
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F

from rest_framework.parsers import JSONParser
from .models import Automelts, AutoMeltsInfo, Daily_gases_consumption, Floattable, Gases_consumptions_per_day, Melttypes, Meltsteps, Substeps, Tagtable 
from .serializers import FloattableSerializer, AutomeltsSerializer

def index(request):
    return Furnace_1_info(request)


def ReportsPage(request):
    template = loader.get_template('FregatMonitoringApp/ReportsPage.html')
    context = None

    return HttpResponse(template.render(context, request))


def GasesUsageReportTemplate(request, **kwards): #Загружает первоначальный шаблон отчёт с данными по умолчанию   
    template = loader.get_template('FregatMonitoringApp/GasesUsage.html')
    
    if(kwards.get('report_type') == 'gases_usage_daily'): #Выбран посуточный отчёт
        start_period = (datetime.now()-timedelta(hours=30*24) ).strftime('%Y-%m-%dT%H:%M')#предыдущий месяц
        stop_period = datetime.now().strftime('%Y-%m-%dT%H:%M')#текущий момент
    elif(kwards.get('report_type') == 'gases_usage_per_day'): #Выбран почасовой отчёт
        start_period = (datetime.now()-timedelta(hours=24)).replace(hour=8,minute=0).strftime('%Y-%m-%dT%H:%M')#предыдущие сутки c 8.00
        stop_period = datetime.now().replace(hour=8,minute=0).strftime('%Y-%m-%dT%H:%M')#текущие сутки до 8.00
 
    context={
        'report_type': kwards.get('report_type'),
        'Start_time': start_period,
        'Stop_time': stop_period,
    }

    return HttpResponse(template.render(context, request))


def getGasesUsageData_hourly(request, **kwards):
    '''Выдаёт данные по запросу клиента за выбранный период по часам. 
       Считает почасовые расходы газов, на основе данных о мгновенных расходах, которые регистрируются в таблице БД FloatTable каждые 10 секунд'''
    
    if request.method == 'GET':
        start_period = datetime.strptime(request.GET['start'], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M') 
        stop_period = datetime.strptime(request.GET['stop'], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M') 
    
    def hourly_db_request(tag_name: Str, start_per, stop_per): #запрос к БД для подсчёта почасового расхода газа(или кислорода) за период
        tag_ind = Tagtable.objects.filter(tagname=tag_name)[0].tagindex #индекс интересующего сигнала
        response_1 = Gases_consumptions_per_day.objects.raw(
            ''' SELECT ROW_NUMBER() OVER(ORDER BY CONCAT(DATEFROMPARTS(DATEPART(year, CAST(DTm AS datetime)), DATEPART(month, CAST(DTm AS datetime)), 
					                                                   DATEPART(day, CAST(DTm AS datetime))
							                                          ), ' ', DATEPART(hour, CAST(DTm AS datetime)),':59')) AS id, 
                       CONCAT(DATEFROMPARTS(DATEPART(year, CAST(DTm AS datetime)), DATEPART(month, CAST(DTm AS datetime)), 
					                        DATEPART(day, CAST(DTm AS datetime))
							               ), ' ', DATEPART(hour, CAST(DTm AS datetime)),':59') AS data, 
                       SUM(TimeDiffVal) AS consumption,
                       (CASE TagName  
                          WHEN 'MEASURES\FL710_NG' THEN 'Gas_P1'
                          WHEN 'MEASURES\TI_810B' THEN 'Gas_P2'
                          WHEN 'MEASURES\O1Flow' THEN 'O2_P1'
                          WHEN 'MEASURES\O2Flow' THEN 'O2_P2'
                          WHEN 'MEASURES\OX_OX800' THEN 'O2_Furma'
                       END) AS GasName 

                FROM(
                     SELECT DATEADD(ms,Millitm,DateAndTime) AS DTm,
                            TagIndex, 
                            (CAST(Val as float)/3600)*DATEDIFF(MILLISECOND,
                                                               DateAdd(ms,Millitm,DateAndTime),
            	                                               DateAdd(ms,
                                                                       LAG(Millitm,1,NULL) OVER (PARTITION BY TagIndex ORDER BY DateAndTime DESC),
            			                                               LAG(DateAndTime,1,NULL) OVER (PARTITION BY TagIndex ORDER BY DateAndTime DESC)
            			                                               )
            	                                               )/1000 as TimeDiffVal
                     FROM [FRGV202X\Production].[FX_Hist].[db_owner].[FloatTable]
                     WHERE TagIndex=%s  AND DateAndTime > %s AND DateAndTime < %s
                     ) a            
                INNER JOIN [FRGV202X\Production].[FX_Hist].[db_owner].[TagTable] b ON a.TagIndex=b.TagIndex
                GROUP BY TagName, CONCAT(DATEFROMPARTS(DATEPART(year, CAST(DTm AS datetime)), DATEPART(month, CAST(DTm AS datetime)), 
					                     DATEPART(day, CAST(DTm AS datetime))
							            ), ' ', DATEPART(hour, CAST(DTm AS datetime)),':59')
                ORDER BY TagName, CAST(CONCAT(DATEFROMPARTS(DATEPART(year, CAST(DTm AS datetime)), DATEPART(month, CAST(DTm AS datetime)), 
					                    DATEPART(day, CAST(DTm AS datetime))
							            ), ' ', DATEPART(hour, CAST(DTm AS datetime)),':59') AS datetime);'''
        , [tag_ind, start_per, stop_per])

        return response_1


    gas_furnace_1_consumption = hourly_db_request('MEASURES\FL710_NG', start_period, stop_period)
    gas_furnace_2_consumption = hourly_db_request('MEASURES\TI_810B', start_period, stop_period)
    o2_furnace_1_consumption = hourly_db_request('MEASURES\O1Flow', start_period, stop_period)
    o2_furnace_2_consumption = hourly_db_request('MEASURES\O2Flow', start_period, stop_period)
    furma_consumption = hourly_db_request('MEASURES\OX_OX800', start_period, stop_period)

    consumptions = list()
    consumptions.append(("furnace_1_Gas", gas_furnace_1_consumption))
    consumptions.append(("furnace_1_O2", o2_furnace_1_consumption))
    consumptions.append(("furnace_2_Gas", gas_furnace_2_consumption))
    consumptions.append(("furnace_2_O2", o2_furnace_2_consumption))
    consumptions.append(("furma", furma_consumption ))

    series = list()
    for i in range(len(consumptions)):
        series.append([[consumptions[i][0]], []])
        for j in range(0, len(consumptions[i][1])):
            point={"date":str(consumptions[i][1][j].data), "value":round(consumptions[i][1][j].consumption, 2)}
            series[i][1].append(point)

    return JsonResponse(series, safe=False)
    

def getGasesUsageData_daily(request, **kwards):
    '''Выдаёт данные по запросу клиента за выбранный период по дням. Достаёт данные из заранее подготовленной таблицы в БД: DailyGasesConsumption.
       Таблица содержит суточные расходы газов, рассчитанные (на основе данных о мгновенных расходах) хранимой процедурой по заданию ежедневно в 23:59'''
      
    if request.method == 'GET':
        start_period = datetime.strptime(request.GET['start'], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d') 
        stop_period = datetime.strptime(request.GET['stop'], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d') 
    else:    
        start_period = (datetime.now()-timedelta(hours=30*24) ).strftime('%Y-%m-%d')#предыдущий месяц
        stop_period = datetime.now().strftime('%Y-%m-%d')#текущий момент
    
    gas_furnace_1_consumption = Daily_gases_consumption.objects.filter(gasname = 'Gas_P1').filter(data__range=(start_period,stop_period)).order_by('data')
    gas_furnace_2_consumption = Daily_gases_consumption.objects.filter(gasname = 'Gas_P2').filter(data__range=(start_period,stop_period)).order_by('data')
    o2_furnace_1_consumption = Daily_gases_consumption.objects.filter(gasname = 'O2_P1').filter(data__range=(start_period,stop_period)).order_by('data')
    o2_furnace_2_consumption = Daily_gases_consumption.objects.filter(gasname = 'O2_P2').filter(data__range=(start_period,stop_period)).order_by('data')
    furma_consumption = Daily_gases_consumption.objects.filter(gasname = 'O2_Furma').filter(data__range=(start_period,stop_period)).order_by('data')

    consumptions = list()
    consumptions.append(("furnace_1_Gas", gas_furnace_1_consumption))
    consumptions.append(("furnace_1_O2", o2_furnace_1_consumption))
    consumptions.append(("furnace_2_Gas", gas_furnace_2_consumption))
    consumptions.append(("furnace_2_O2", o2_furnace_2_consumption))
    consumptions.append(("furma", furma_consumption ))

    series = list()
    for i in range(len(consumptions)):
        series.append([[consumptions[i][0]], []])
        for j in range(0, len(consumptions[i][1])):
            ts = datetime.strptime(str(consumptions[i][1][j].data), "%Y-%m-%d")
            point={"date":str(consumptions[i][1][j].data), "timestamp":ts.timestamp()*1000, "value":round(consumptions[i][1][j].daily_consumption, 2)}
            point={"date":str(consumptions[i][1][j].data), "value":round(consumptions[i][1][j].daily_consumption, 2)}
            series[i][1].append(point)

    return JsonResponse(series, safe=False)


def FurnaceBaseTrends(request, Furnace_No, **kwards):  #отображает шаблон экрана трендов для печи
    template = loader.get_template('FregatMonitoringApp/FurnaceTrendsPage.html')
    if(kwards.get('start_time') is not None and kwards.get('stop_time') is not None):
        start_period = kwards.get('start_time') 
        stop_period = kwards.get('stop_time')
    else:    
        start_period = (datetime.now()-timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')#предыдущий час
        stop_period = datetime.now().strftime('%Y-%m-%dT%H:%M')#текущий момент
    context = {
        'Furnace_No': Furnace_No,
        'Start_time': start_period,
        'Stop_time': stop_period
    }
    return HttpResponse(template.render(context, request))


def FurnaceBaseTrendsData(request, Furnace_No): #готовит и отправляет данные сигналов для трендов за указанный период времени
    if request.method == 'GET':
        start_period = request.GET['start']
        stop_period = request.GET['stop']

    def LoadSignalValuesByPeriod(signal_name, period_start, period_stop, **kwards):
        #возвращает выборку значений сигналов с метками времени за определённый период времени
        minus_mod = kwards.get('minus') if kwards.get('minus') is not None else 0 #опция для сигналов положения дросселей, которые нужно дешифровать, отнимая определённое число
        signal_value = Floattable.objects.annotate(value=F('val')-minus_mod).filter(
                        tagindex=Tagtable.objects.filter(tagname=signal_name)[0].tagindex
                        ).filter(dateandtime__range=(period_start,period_stop)).order_by('dateandtime')
        return signal_value
    
    #Список сигналов, отображаемых на тренде. Чтобы добавить новый сигнал, нужно внести для него строку в этот блок
    signals = list()

    #сигналы для первой печи
    if Furnace_No == 1:
        signals.append(("Мощность", LoadSignalValuesByPeriod('MEASURES\HY_F711', start_period, stop_period)))
        signals.append(("Ток двигателя", LoadSignalValuesByPeriod('MEASURES\SI_KL710', start_period, stop_period)))
        signals.append(("Расход газа", LoadSignalValuesByPeriod('MEASURES\FL710_NG', start_period, stop_period)))
        signals.append(("Расход О2", LoadSignalValuesByPeriod('MEASURES\O1Flow', start_period, stop_period)))
        signals.append(("Расход воздуха", LoadSignalValuesByPeriod('MEASURES\FL710_AIR', start_period, stop_period)))
        signals.append(("Альфа", LoadSignalValuesByPeriod('MEASURES\Alpha_p1', start_period, stop_period)))
        signals.append(("Лямбда", LoadSignalValuesByPeriod('MEASURES\Lambda_p1', start_period, stop_period)))
        signals.append(("Круглый дроссель", LoadSignalValuesByPeriod('MEASURES\p1_mct1_rez', start_period, stop_period, minus=256)))
        signals.append(("На 3 фильтр", LoadSignalValuesByPeriod('MEASURES\p1_mct5_rez', start_period, stop_period, minus=1280)))
        signals.append(("Над дверью", LoadSignalValuesByPeriod('MEASURES\p1_mct2_rez', start_period, stop_period, minus=512)))
        signals.append(("Горячий дроссель", LoadSignalValuesByPeriod('MEASURES\ZI_701', start_period, stop_period)))
        signals.append(("dP на фильтре", LoadSignalValuesByPeriod('MEASURES\PDI_720', start_period, stop_period)))
        signals.append(("dP на дымососе", LoadSignalValuesByPeriod('MEASURES\PDI_724', start_period, stop_period)))
        signals.append(("Частота дымососа", LoadSignalValuesByPeriod('MEASURES\SI_U720', start_period, stop_period)))
        signals.append(("Т перед фильтром", LoadSignalValuesByPeriod('MEASURES\TI_704', start_period, stop_period)))

        signals.append(("Т над дверью", LoadSignalValuesByPeriod('MEASURES\TI_712Y', start_period, stop_period))) #эти два сигнала должны быть в списке последними
        signals.append(("Т воздух цех", LoadSignalValuesByPeriod('MEASURES\TI_712X', start_period, stop_period))) #эти два сигнала должны быть в списке последними

    elif Furnace_No == 2:
        signals.append(("Мощность", LoadSignalValuesByPeriod('MEASURES\HY_F710', start_period, stop_period)))
        signals.append(("Ток двигателя", LoadSignalValuesByPeriod('MEASURES\SI_KL711', start_period, stop_period)))
        signals.append(("Расход газа", LoadSignalValuesByPeriod('MEASURES\TI_810B', start_period, stop_period)))
        signals.append(("Расход О2", LoadSignalValuesByPeriod('MEASURES\O2Flow', start_period, stop_period)))
        signals.append(("Расход воздуха", LoadSignalValuesByPeriod('MEASURES\TI_810C', start_period, stop_period)))
        signals.append(("Альфа", LoadSignalValuesByPeriod('MEASURES\Alpha', start_period, stop_period)))
        signals.append(("Лямбда", LoadSignalValuesByPeriod('MEASURES\Lambda', start_period, stop_period)))
        signals.append(("Круглый дроссель", LoadSignalValuesByPeriod('MEASURES\\xvi_v_cech', start_period, stop_period)))
        signals.append(("На 3 фильтр", LoadSignalValuesByPeriod('MEASURES\XVI_708', start_period, stop_period)))
        signals.append(("Над дверью", LoadSignalValuesByPeriod('MEASURES\ZI_704', start_period, stop_period)))
        signals.append(("Горячий дроссель", LoadSignalValuesByPeriod('MEASURES\PY_702', start_period, stop_period)))
        signals.append(("dP на фильтре", LoadSignalValuesByPeriod('MEASURES\PDI_725', start_period, stop_period)))
        signals.append(("dP на дымососе", LoadSignalValuesByPeriod('MEASURES\PDI_729', start_period, stop_period)))
        signals.append(("Частота дымососа", LoadSignalValuesByPeriod('MEASURES\SI_U721', start_period, stop_period)))
        signals.append(("Т перед фильтром", LoadSignalValuesByPeriod('MEASURES\TI_708', start_period, stop_period)))

        signals.append(("Т над дверью", LoadSignalValuesByPeriod('MEASURES\TI_711Y', start_period, stop_period))) #эти два сигнала должны быть в списке последними
        signals.append(("Т воздух цех", LoadSignalValuesByPeriod('MEASURES\TI_711X', start_period, stop_period))) #эти два сигнала должны быть в списке последними

    detalization = 1

    series = list()
    for i in range(len(signals)):
        if signals[i][0] not in {"Т над дверью","Т воздух цех"}: #для случая вычисления разности(или другой операции) между двумя сигналами
            series.append([[signals[i][0]], []])
            for j in range(0, len(signals[i][1]), detalization):
                dat = datetime.strptime(str(signals[i][1][j].dateandtime), '%Y-%m-%d %H:%M:%S+00:00')
                point={"date":dat.timestamp()*1000, "value":round(signals[i][1][j].value, 2)}
                series[i][1].append(point)
        elif signals[i][0] in {"Т над дверью"}: #исключение для вычисления дельты температур
            series.append([["Дельта Т"], []])
            for a,b in itertools.zip_longest(signals[i][1], signals[i+1][1]): #шагаем сразу по двум спискам. Для ускорения вычислений
                dat = datetime.strptime(str(a.dateandtime), '%Y-%m-%d %H:%M:%S+00:00')
                point={"date":dat.timestamp()*1000, "value":round(a.value-b.value, 2)}
                series[i][1].append(point)

    return JsonResponse(series, safe=False)


def error_message(request):
    template = loader.get_template('FregatMonitoringApp/ErrorMessage.html')
    context = None
    return HttpResponse(template.render(context, request))


def sorry_page(request):
    template = loader.get_template('FregatMonitoringApp/SorryPage.html')
    context = None
    return HttpResponse(template.render(context, request))


def Furnace_1_info(request):
    
    #горелка
    
    power_sp = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\HY_F711')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\HY_F711')[0].tagindex]
    gas_flow = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\FL710_NG')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\FL710_NG')[0].tagindex]
    air_flow = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\FL710_AIR')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\FL710_AIR')[0].tagindex]
    o2_flow =  [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\O1Flow')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\O1Flow')[0].tagindex]
    alpha = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\Alpha_p1')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\Alpha_p1')[0].tagindex]
    lambd = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\Lambda_p1')[0].tagindex).order_by('-dateandtime')[0].val,2),
    Tagtable.objects.filter(tagname='MEASURES\Lambda_p1')[0].tagindex]
    standby = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='GENERAL\F710_LOCK')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='GENERAL\F710_LOCK')[0].tagindex]
    power_mode = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\HS1_F710')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='IO\HS1_F710')[0].tagindex]
    

    #горячий газоход
    hotflue_p = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PI_701')[0].tagindex).order_by('-dateandtime')[0].val,1),
    Tagtable.objects.filter(tagname='MEASURES\PI_701')[0].tagindex]
    hotflue_t = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_703B')[0].tagindex).order_by('-dateandtime')[0].val,1),
    Tagtable.objects.filter(tagname='MEASURES\TI_703B')[0].tagindex]
    
    #фильтр
    filter_dp = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PDI_720')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\PDI_720')[0].tagindex] 
    t_before_filter = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_704')[0].tagindex).order_by('-dateandtime')[0].val,1), 
    Tagtable.objects.filter(tagname='MEASURES\TI_704')[0].tagindex]
    
    #дымосос
    exhauster_dp = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PDI_724')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\PDI_724')[0].tagindex]
    exhauster_pc = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SI_U720')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='MEASURES\SI_U720')[0].tagindex]

    #дроссели
    hot_flue_gate = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\ZI_701')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\ZI_701')[0].tagindex]
    over_door_gate = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\p1_mct2_rez')[0].tagindex).order_by('-dateandtime')[0].val - 512),
    Tagtable.objects.filter(tagname='MEASURES\p1_mct2_rez')[0].tagindex]
    exhauster_gate = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\p1_mct7_rez')[0].tagindex).order_by('-dateandtime')[0].val - 1792,
    Tagtable.objects.filter(tagname='MEASURES\p1_mct7_rez')[0].tagindex]
    round_gate = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\p1_mct1_rez')[0].tagindex).order_by('-dateandtime')[0].val - 256,
    Tagtable.objects.filter(tagname='MEASURES\p1_mct1_rez')[0].tagindex]
    filter3_gate = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\p1_mct5_rez')[0].tagindex).order_by('-dateandtime')[0].val - 1280,
    Tagtable.objects.filter(tagname='MEASURES\p1_mct5_rez')[0].tagindex]
    drain_gate = ["открыт" if not Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='VALVES\XV701_ZL')[0].tagindex).order_by('-dateandtime')[0].val else "закрыт",
    Tagtable.objects.filter(tagname='VALVES\XV701_ZL')[0].tagindex]

    #дельта
    over_door_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_712Y')[0].tagindex).order_by('-dateandtime')[0].val
    cold_air_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_712X')[0].tagindex).order_by('-dateandtime')[0].val
    deltaT = round(over_door_t - cold_air_t,1)

    #печь
    furnace_rotation = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SY_KL710')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\SY_KL710')[0].tagindex]
    furnace_current = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SI_KL710')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\SI_KL710')[0].tagindex]
    loading_door_half = ["открыта" if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='VALVES\XVF710P_ZL')[0].tagindex).order_by('-dateandtime')[0].val == 0 else "закрыта",
    Tagtable.objects.filter(tagname='VALVES\XVF710P_ZL')[0].tagindex]
    
    #поезд - не прописан в History
    #train_move = "Едет" if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MOTORS\H750_FB')[0].tagindex).order_by('-dateandtime')[0].val else "Стоит"
    #train_fwd = "вперёд" if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MOTORS\H750_FWB')[0].tagindex).order_by('-dateandtime')[0].val else "назад"
    #train_fwd = train_fwd if train_move else "---"

    #шзм - не прописан в History
    try:
        if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\ZSL_PK710')[0].tagindex).order_by('-dateandtime')[0].val:
            shzm_position = "У поля"
        elif Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\ZSH_PK710')[0].tagindex).order_by('-dateandtime')[0].val:
            shzm_position = "У 1 печи"
        elif Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\ZSHH_PK710')[0].tagindex).order_by('-dateandtime')[0].val:
            shzm_position = "У 2 печи"
    except:
        shzm_position = "---"

    weight_in_shzm= [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\WI_710')[0].tagindex).order_by('-dateandtime')[0].val,2),
    Tagtable.objects.filter(tagname='MEASURES\WI_710')[0].tagindex]

    #автоплавка
    Automelt_info = Automelts.objects.filter(furnace_no=1)
    auto_mode = "Автомат" if Automelt_info[0].auto_mode else "Ручной"
    try:
        meltid = Melttypes.objects.filter(melt_num = Automelt_info[0].melt_type).filter(melt_furnace = Automelt_info[0].furnace_no)[0].melt_id
    except:
        meltid = "---"
    try:
        melt_type = Melttypes.objects.filter(melt_id = meltid)[0].melt_name
    except:
        melt_type = "---"
    try:
        melt_step = Meltsteps.objects.filter(melt = meltid).filter(step_num = Automelt_info[0].melt_step)[0].step_name
    except:
        melt_step = "---"
    step_total_time = Automelt_info[0].step_total_time
    step_time_remain = step_total_time - Automelt_info[0].step_time_remain
    deltat_stp = Automelt_info[0].deltat

    template = loader.get_template('FregatMonitoringApp/furnace_info.html')
    context = {'furnace_num': 1,
               'power_sp': power_sp,
               'gas_flow': gas_flow,
               'air_flow': air_flow,
               'o2_flow': o2_flow,
               'alpha': alpha,
               'lambda': lambd,
               'standby': standby,
               'power_mode': power_mode,
               'filter_dp': filter_dp,
               'exhauster_dp': exhauster_dp,
               't_before_filter': t_before_filter,
               'hotflue_p': hotflue_p,
               'hotflue_t': hotflue_t,
               'exhauster_pc': exhauster_pc,
               'hot_flue_gate': hot_flue_gate,
               'over_door_gate': over_door_gate,
               'exhauster_gate': exhauster_gate,
               'round_gate': round_gate,
               'filter3_gate': filter3_gate,
               'drain_gate': drain_gate,    
               'over_door_t': over_door_t,
               'cold_air_t': cold_air_t,
               'deltaT': deltaT,
               'furnace_rotation': furnace_rotation,
               'furnace_current': furnace_current,
               'loading_door_half': loading_door_half,
               'auto_mode': auto_mode,
               'melt_type' : melt_type,
               'melt_step' : melt_step,
               'step_total_time' : step_total_time,
               'step_time_remain' : step_time_remain,
               'deltat_stp' : deltat_stp,
               'shzm_position': shzm_position,
               'weight_in_shzm': weight_in_shzm,
              }

    return HttpResponse(template.render(context, request))


def Furnace_2_info(request):
    
    #горелка
    power_sp = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\HY_F710')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\HY_F710')[0].tagindex]
    gas_flow = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_810B')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\TI_810B')[0].tagindex]
    air_flow = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_810C')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\TI_810C')[0].tagindex]
    o2_flow =  [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\O2Flow')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\O2Flow')[0].tagindex]
    alpha = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\Alpha')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\Alpha')[0].tagindex]
    lambd = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\Lambda')[0].tagindex).order_by('-dateandtime')[0].val,2),
    Tagtable.objects.filter(tagname='MEASURES\Lambda')[0].tagindex]
    standby = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='GENERAL\F711_LOCK')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='GENERAL\F711_LOCK')[0].tagindex]
    power_mode = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\HS1_F711')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='IO\HS1_F711')[0].tagindex]
    

    #горячий газоход
    hotflue_p = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PI_702')[0].tagindex).order_by('-dateandtime')[0].val,1),
    Tagtable.objects.filter(tagname='MEASURES\PI_702')[0].tagindex]
    hotflue_t = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_705A')[0].tagindex).order_by('-dateandtime')[0].val,1),
    Tagtable.objects.filter(tagname='MEASURES\TI_705A')[0].tagindex]
    
    #фильтр
    filter_dp = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PDI_725')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\PDI_725')[0].tagindex] 
    t_before_filter = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_708')[0].tagindex).order_by('-dateandtime')[0].val,1), 
    Tagtable.objects.filter(tagname='MEASURES\TI_708')[0].tagindex]
    
    #дымосос
    exhauster_dp = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PDI_729')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\PDI_729')[0].tagindex]
    exhauster_pc = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SI_U721')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='MEASURES\SI_U721')[0].tagindex]

    #дроссели
    hot_flue_gate = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PY_702')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\PY_702')[0].tagindex]
    over_door_gate = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\ZI_704')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='MEASURES\ZI_704')[0].tagindex]
    exhauster_gate = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\ZI_706')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='MEASURES\ZI_706')[0].tagindex]
    round_gate = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\\xvi_v_cech')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='MEASURES\\xvi_v_cech')[0].tagindex]
    filter3_gate = [Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\XVI_708')[0].tagindex).order_by('-dateandtime')[0].val,
    Tagtable.objects.filter(tagname='MEASURES\XVI_708')[0].tagindex]
    drain_gate = ["открыт" if not Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='VALVES\XV702_ZL')[0].tagindex).order_by('-dateandtime')[0].val else "закрыт",
    Tagtable.objects.filter(tagname='VALVES\XV702_ZL')[0].tagindex]

    #дельта
    over_door_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_711Y')[0].tagindex).order_by('-dateandtime')[0].val
    cold_air_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_711X')[0].tagindex).order_by('-dateandtime')[0].val
    deltaT = round(over_door_t - cold_air_t,1)

    #печь
    furnace_rotation = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SY_KL711')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\SY_KL711')[0].tagindex]
    furnace_current = [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SI_KL711')[0].tagindex).order_by('-dateandtime')[0].val),
    Tagtable.objects.filter(tagname='MEASURES\SI_KL711')[0].tagindex]
    loading_door_half = ["открыта" if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='VALVES\XVF711P_ZL')[0].tagindex).order_by('-dateandtime')[0].val == 0 else "закрыта",
    Tagtable.objects.filter(tagname='VALVES\XVF711P_ZL')[0].tagindex]
    
    #поезд - не прописан в History
    #train_move = "Едет" if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MOTORS\H750_FB')[0].tagindex).order_by('-dateandtime')[0].val else "Стоит"
    #train_fwd = "вперёд" if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MOTORS\H750_FWB')[0].tagindex).order_by('-dateandtime')[0].val else "назад"
    #train_fwd = train_fwd if train_move else "---"

    #шзм - не прописан в History
    try:
        if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\ZSL_PK710')[0].tagindex).order_by('-dateandtime')[0].val:
            shzm_position = "У поля"
        elif Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\ZSH_PK710')[0].tagindex).order_by('-dateandtime')[0].val:
            shzm_position = "У 1 печи"
        elif Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\ZSHH_PK710')[0].tagindex).order_by('-dateandtime')[0].val:
            shzm_position = "У 2 печи"
    except:
        shzm_position = "---"

    weight_in_shzm= [round(Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\WI_710')[0].tagindex).order_by('-dateandtime')[0].val,2),
    Tagtable.objects.filter(tagname='MEASURES\WI_710')[0].tagindex]

    #автоплавка
    Automelt_info = Automelts.objects.filter(furnace_no=2)
    auto_mode = "Автомат" if Automelt_info[0].auto_mode else "Ручной"
    try:
        meltid = Melttypes.objects.filter(melt_num = Automelt_info[0].melt_type).filter(melt_furnace = Automelt_info[0].furnace_no)[0].melt_id
    except:
        meltid = "---"
    try:
        melt_type = Melttypes.objects.filter(melt_id = meltid)[0].melt_name
    except:
        melt_type = "---"
    try:
        melt_step = Meltsteps.objects.filter(melt = meltid).filter(step_num = Automelt_info[0].melt_step)[0].step_name
    except:
        melt_step = "---"
    step_total_time = Automelt_info[0].step_total_time
    step_time_remain = step_total_time - Automelt_info[0].step_time_remain
    deltat_stp = Automelt_info[0].deltat

    template = loader.get_template('FregatMonitoringApp/furnace_info.html')
    context = {'furnace_num': 2,
               'power_sp': power_sp,
               'gas_flow': gas_flow,
               'air_flow': air_flow,
               'o2_flow': o2_flow,
               'alpha': alpha,
               'lambda': lambd,
               'standby': standby,
               'power_mode': power_mode,
               'filter_dp': filter_dp,
               'exhauster_dp': exhauster_dp,
               't_before_filter': t_before_filter,
               'hotflue_p': hotflue_p,
               'hotflue_t': hotflue_t,
               'exhauster_pc': exhauster_pc,
               'hot_flue_gate': hot_flue_gate,
               'over_door_gate': over_door_gate,
               'exhauster_gate': exhauster_gate,
               'round_gate': round_gate,
               'filter3_gate': filter3_gate,
               'drain_gate': drain_gate,    
               'over_door_t': over_door_t,
               'cold_air_t': cold_air_t,
               'deltaT': deltaT,
               'furnace_rotation': furnace_rotation,
               'furnace_current': furnace_current,
               'loading_door_half': loading_door_half,
               'auto_mode': auto_mode,
               'melt_type' : melt_type,
               'melt_step' : melt_step,
               'step_total_time' : step_total_time,
               'step_time_remain' : step_time_remain,
               'deltat_stp' : deltat_stp,
               'shzm_position': shzm_position,
               'weight_in_shzm' : weight_in_shzm,
              }

    return HttpResponse(template.render(context, request))


def AutoMeltTypes_info(request, meltID_1):

    melt_type_list_1 = Melttypes.objects.filter(melt_furnace=1) #Выбираем типы плавок для первой печи(для второй такие же)
    melt_type_list_2 = Melttypes.objects.filter(melt_furnace=2)

    melt_type_name = Melttypes.objects.filter(melt_id=meltID_1)[0].melt_name #Узнаём, как называется этот тип плавки
    meltID_2 = Melttypes.objects.filter(melt_name=melt_type_name, melt_furnace=2)[0].melt_id #По имени вытаскиваем id аналогичной плавки для второй печи

     
    melt_steps_list_1 = Meltsteps.objects.filter(melt=meltID_1) #Выбираем шаги для нужных плавок
    melt_steps_list_2 = Meltsteps.objects.filter(melt=meltID_2)
    
    #Выбираем подшаги для каждого шага каждой плавки
    substeps_list_1 = list() 
    for melt_step in melt_steps_list_1: 
        for substep in [Substeps.objects.filter(step=melt_step.step_id)]:
            substeps_list_1.extend(substep)

    substeps_list_2 = list()
    for melt_step in melt_steps_list_2: 
        for substep in [Substeps.objects.filter(step=melt_step.step_id)]:
            substeps_list_2.extend(substep)

    template = loader.get_template('FregatMonitoringApp/AutoMeltTypes_info.html')
    context = {
        'melts_id': [meltID_1, meltID_2],
        'melt_types_1': melt_type_list_1,
        'melt_types_2': melt_type_list_2,
        'melt_steps_1': melt_steps_list_1,
        'melt_steps_2': melt_steps_list_2,
        'substeps_1' : substeps_list_1,
        'substeps_2' : substeps_list_2
    }

    return HttpResponse(template.render(context, request))


def AutoMelts_SetPoints(request):
    
    template = loader.get_template('FregatMonitoringApp/AutoMeltsSetPoints.html')
    try:
        deltaT1_stp = Automelts.objects.filter(furnace_no=1)[0].deltat
        deltaT2_stp = Automelts.objects.filter(furnace_no=2)[0].deltat
    except:
        return error_message(request) #Ой, что-то пошло не так
    
    context={
        'deltaT1_stp':deltaT1_stp,
        'deltaT2_stp':deltaT2_stp,
    }
    return HttpResponse(template.render(context, request))


def AutoMeltsSaveSettings(request, meltID_1, meltID_2): #сохраняет изменение режимов автоплаки в базе
    
    melt_steps_list = Meltsteps.objects.filter(melt__in=[meltID_1, meltID_2]) #Выбираем шаги для нужных плавок

    #Выбираем подшаги для каждого шага каждой плавки
    for melt_step in melt_steps_list: 
        for substep in Substeps.objects.filter(step=melt_step.step_id):
            try:
                substep.sub_step_time = request.POST["Time_substepid_"+str(substep.substep_id)] if request.POST["Time_substepid_"+str(substep.substep_id)]!="" else None
                substep.power_sp = request.POST["Power_substepid_"+str(substep.substep_id)] if request.POST["Power_substepid_"+str(substep.substep_id)]!="" else None
                substep.rotation_sp = request.POST["Rotation_substepid_"+str(substep.substep_id)] if request.POST["Rotation_substepid_"+str(substep.substep_id)]!="" else None
                substep.alpha_sp = request.POST["Alpha_substepid_"+str(substep.substep_id)] if request.POST["Alpha_substepid_"+str(substep.substep_id)]!="" else None
            except (KeyError, substep.DoesNotExist):
                return error_message(request) #Ой, что-то пошло не так
            else:
                substep.save()

    return HttpResponseRedirect(reverse('FregatMonitoringApp:Automelts_info', args=(meltID_1,)))


def AutoMeltsSaveSetpoints(request, furnace_num): #сохраняет изменение уставки Дельты в базе
    try:
        try: 
            float(request.POST["DeltaT"+str(furnace_num)+"_stp"]) #"Это число вообще?"
        except:
            return error_message(request) #Ой, что-то пошло не так
        Melt = Automelts.objects.filter(furnace_no = furnace_num)[0]
        Melt.deltat = request.POST["DeltaT"+str(furnace_num)+"_stp"]
    except: #не удалось записать в базу
        return error_message(request) #Ой, что-то пошло не так
    else:
        Melt.save() 

    return HttpResponseRedirect(reverse('FregatMonitoringApp:AutoMeltsSetPoints'))


#----------ОТОБРАЖЕНИЯ ЧЕРЕЗ СЕРИАЛАЙЗЕРЫ-------------------

def Furnace_info_s(request, SignalIndex): # API для обновления данных на экране "Печь 1(2)"
    
    #В общем виде ищем последнее значение в таблице для каждого сигнала
    tag_val = Floattable.objects.filter(tagindex=SignalIndex).order_by('-dateandtime')[:1]

    serializer = FloattableSerializer(tag_val, many=True)

    # если значение сигнала нужно пред-обработать, обрабатываем значение уже внутри сериалайзера
    #----Исключения 1 печь----------------
    if SignalIndex == 13: #нагрузка на печь
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)
    if SignalIndex == 51: #вращение печи
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)
    if SignalIndex == 52: #дроссель горячего газохода
        serializer.data[0]['val'] = round(serializer.data[0]['val'],0)
    if SignalIndex == 25: #температура гор.газохода
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)
    if SignalIndex == 26: #температура перед фильтром
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)
    if SignalIndex == 115: #лямбда
        serializer.data[0]['val'] = round(serializer.data[0]['val'],2)
    if SignalIndex == 85: #сливной дроссель
        serializer.data[0]['val'] = "открыт" if not serializer.data[0]['val'] else "закрыт"
    if SignalIndex == 117: #дроссель круглый
        serializer.data[0]['val'] = serializer.data[0]['val']-256
    if SignalIndex == 118: #дроссель над дверью
        serializer.data[0]['val'] = serializer.data[0]['val']-512
    if SignalIndex == 121: #дроссель на 3 фильтр
        serializer.data[0]['val'] = serializer.data[0]['val']-1280
    if SignalIndex == 123: #дроссель дымососа
        serializer.data[0]['val'] = serializer.data[0]['val']-1792

    #----Исключения 1 печь----------------
    if SignalIndex == 14: #нагрузка на печь
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)
    if SignalIndex == 17: #вращение печи
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)
    if SignalIndex == 75: #дроссель горячего газохода
        serializer.data[0]['val'] = round(serializer.data[0]['val'],0)
    if SignalIndex == 27: #температура гор.газохода
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)
    if SignalIndex == 31: #температура перед фильтром
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)
    if SignalIndex == 63: #лямбда
        serializer.data[0]['val'] = round(serializer.data[0]['val'],2)
    if SignalIndex == 81: #сливной дроссель
        serializer.data[0]['val'] = "открыт" if not serializer.data[0]['val'] else "закрыт"
    if SignalIndex == 9: #перепад на дымососе
        serializer.data[0]['val'] = round(serializer.data[0]['val'])
    if SignalIndex == 12: #разряжение в гор. газоходе
        serializer.data[0]['val'] = round(serializer.data[0]['val'],1)

    #----Исключения ШЗМ---------------
    if SignalIndex == 48: #вес в бункере ШЗМ
        serializer.data[0]['val'] = round(serializer.data[0]['val'],2)

    return JsonResponse(serializer.data, safe=False)


def Furnace_info_a(request, FurnaceNo): # API для обновления данных о автоплавке на экране "Печь 1(2)"

    melt_inst = Automelts.objects.filter(furnace_no=FurnaceNo)[0]
    melt_type_inst = Melttypes.objects.filter(melt_num = melt_inst.melt_type)[0]
    step_type_inst = Meltsteps.objects.filter(step_num = melt_inst.melt_step).filter(melt = melt_type_inst.melt_id)[0]

    #дельта
    if FurnaceNo == 1:
        over_door_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_712Y')[0].tagindex).order_by('-dateandtime')[0].val
        cold_air_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_712X')[0].tagindex).order_by('-dateandtime')[0].val
    elif FurnaceNo == 2:
        over_door_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_711Y')[0].tagindex).order_by('-dateandtime')[0].val
        cold_air_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_711X')[0].tagindex).order_by('-dateandtime')[0].val
    deltaT = over_door_t - cold_air_t
    
    AMmodel = AutoMeltsInfo(
        furnace_no = FurnaceNo,
        auto_mode = "Автомат" if melt_inst.auto_mode else "Ручной",
        melt_name = melt_type_inst.melt_name,
        step_name = step_type_inst.step_name,
        step_total_time = melt_inst.step_total_time,
        step_time_remain = melt_inst.step_total_time - melt_inst.step_time_remain,
        deltat = round(deltaT,1),
        deltat_stp = melt_inst.deltat
    )

    serializer = AutomeltsSerializer(AMmodel)

    return JsonResponse(serializer.data, safe=False)
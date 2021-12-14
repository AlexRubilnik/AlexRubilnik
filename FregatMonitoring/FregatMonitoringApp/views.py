from django import template
from django.db.models.query_utils import subclasses
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context, loader
from django.urls import reverse

from .models import Floattable, Tagtable, Automelts
from .models import Melttypes, Meltsteps, Substeps

def index(request):
    template = loader.get_template('FregatMonitoringApp/base.html')
    context = None
    return HttpResponse(template.render(context, request))

def error_message(request):
    template = loader.get_template('FregatMonitoringApp/ErrorMessage.html')
    context = None
    return HttpResponse(template.render(context, request))

def sorry_page(request):
    template = loader.get_template('FregatMonitoringApp/SorryPage.html')
    context = None
    return HttpResponse(template.render(context, request))

def Furnace_1_info(request):
    
    tag_list = list()
    tag_list.append(['Задание мощности', Tagtable.objects.filter(tagname='MEASURES\HY_F711')[0].tagindex])
    tag_list.append(['Расход газа', Tagtable.objects.filter(tagname='MEASURES\FL710_NG')[0].tagindex])
    tag_list.append(['Расход воздуха', Tagtable.objects.filter(tagname='MEASURES\FL710_AIR')[0].tagindex])
    tag_list.append(['Расход кислорода', Tagtable.objects.filter(tagname='MEASURES\O1Flow')[0].tagindex])
    tag_list.append(['Альфа', Tagtable.objects.filter(tagname='MEASURES\Alpha_p1')[0].tagindex])
    tag_list.append(['Лямбда', Tagtable.objects.filter(tagname='MEASURES\Lambda_p1')[0].tagindex])
    tag_list.append(['Перепад на фильтре', Tagtable.objects.filter(tagname='MEASURES\PDI_720')[0].tagindex])
    tag_list.append(['Перепад на дымососе', Tagtable.objects.filter(tagname='MEASURES\PDI_724')[0].tagindex])
    tag_list.append(['Разяряжение в гор. газоходе', Tagtable.objects.filter(tagname='MEASURES\PI_701')[0].tagindex])
    tag_list.append(['Частота ПЧ дымососа', Tagtable.objects.filter(tagname='MEASURES\SI_U720')[0].tagindex])

    for tag in tag_list:
        tag.append(Floattable.objects.filter(tagindex=tag[1]).order_by('-dateandtime')[0].val)

    #горелка
    power_sp = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\HY_F711')[0].tagindex).order_by('-dateandtime')[0].val
    gas_flow = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\FL710_NG')[0].tagindex).order_by('-dateandtime')[0].val
    air_flow = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\FL710_AIR')[0].tagindex).order_by('-dateandtime')[0].val
    o2_flow =  Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\O1Flow')[0].tagindex).order_by('-dateandtime')[0].val
    alpha = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\Alpha_p1')[0].tagindex).order_by('-dateandtime')[0].val
    lambd = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\Lambda_p1')[0].tagindex).order_by('-dateandtime')[0].val
    standby = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='GENERAL\F710_LOCK')[0].tagindex).order_by('-dateandtime')[0].val
    power_mode = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\HS1_F710')[0].tagindex).order_by('-dateandtime')[0].val

    #горячий газоход
    hotflue_p = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PI_701')[0].tagindex).order_by('-dateandtime')[0].val
    hotflue_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_703B')[0].tagindex).order_by('-dateandtime')[0].val

    #фильтр
    filter_dp = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PDI_720')[0].tagindex).order_by('-dateandtime')[0].val 
    t_before_filter = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_704')[0].tagindex).order_by('-dateandtime')[0].val 
    #дымосос
    exhauster_dp = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PDI_724')[0].tagindex).order_by('-dateandtime')[0].val
    exhauster_pc = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SI_U720')[0].tagindex).order_by('-dateandtime')[0].val
    #дроссели
    hot_flue_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\ZI_701')[0].tagindex).order_by('-dateandtime')[0].val
    over_door_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\p1_mct2_rez')[0].tagindex).order_by('-dateandtime')[0].val - 512
    exhauster_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\p1_mct7_rez')[0].tagindex).order_by('-dateandtime')[0].val - 1792
    round_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\p1_mct1_rez')[0].tagindex).order_by('-dateandtime')[0].val - 256
    filter3_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\p1_mct5_rez')[0].tagindex).order_by('-dateandtime')[0].val - 1280
    drain_gate = "открыт" if not Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='VALVES\XV701_ZL')[0].tagindex).order_by('-dateandtime')[0].val else "закрыт"

    #дельта
    over_door_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_712Y')[0].tagindex).order_by('-dateandtime')[0].val
    cold_air_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_712X')[0].tagindex).order_by('-dateandtime')[0].val
    deltaT = over_door_t - cold_air_t

    #печь
    furnace_rotation = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SY_KL710')[0].tagindex).order_by('-dateandtime')[0].val
    furnace_current = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SI_KL710')[0].tagindex).order_by('-dateandtime')[0].val
    loading_door_half = "открыта" if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='VALVES\XVF710P_ZL')[0].tagindex).order_by('-dateandtime')[0].val == 0 else "закрыта"
    
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
    step_time_remain = Automelt_info[0].step_time_remain
    deltat_stp = Automelt_info[0].deltat

    template = loader.get_template('FregatMonitoringApp/furnace_info.html')
    context = {'furnace_num': 1,
               'power_sp': round(power_sp),
               'gas_flow': round(gas_flow),
               'air_flow': round(air_flow),
               'o2_flow': round(o2_flow),
               'alpha': round(alpha),
               'lambda': round(lambd,2),
               'standby': standby,
               'power_mode': power_mode,
               'filter_dp': round(filter_dp),
               'exhauster_dp': round(exhauster_dp),
               't_before_filter': round(t_before_filter,1),
               'hotflue_p': round(hotflue_p),
               'hotflue_t': round(hotflue_t,1),
               'exhauster_pc': round(exhauster_pc,1),
               'hot_flue_gate': round(hot_flue_gate),
               'over_door_gate': round(over_door_gate),
               'exhauster_gate': round(exhauster_gate),
               'round_gate': round(round_gate),
               'filter3_gate': round(filter3_gate),
               'drain_gate': drain_gate,    
               'over_door_t': round(over_door_t),
               'cold_air_t': round(cold_air_t,1),
               'deltaT': round(deltaT,1),
               'furnace_rotation': round(furnace_rotation, 1),
               'furnace_current': round(furnace_current,1),
               'loading_door_half': loading_door_half,
               'auto_mode': auto_mode,
               'melt_type' : melt_type,
               'melt_step' : melt_step,
               'step_total_time' : step_total_time,
               'step_time_remain' : step_time_remain,
               'deltat_stp' : deltat_stp,
               'shzm_position': shzm_position,
              }

    return HttpResponse(template.render(context, request))

def Furnace_2_info(request):
    
    tag_list = list()
    tag_list.append(['Задание мощности', Tagtable.objects.filter(tagname='MEASURES\HY_F710')[0].tagindex])
    tag_list.append(['Расход газа', Tagtable.objects.filter(tagname='MEASURES\TI_810B')[0].tagindex])
    tag_list.append(['Расход воздуха', Tagtable.objects.filter(tagname='MEASURES\TI_810C')[0].tagindex])
    tag_list.append(['Расход кислорода', Tagtable.objects.filter(tagname='MEASURES\O2Flow')[0].tagindex])
    tag_list.append(['Альфа', Tagtable.objects.filter(tagname='MEASURES\Alpha')[0].tagindex])
    tag_list.append(['Лямбда', Tagtable.objects.filter(tagname='MEASURES\Lambda')[0].tagindex])
    tag_list.append(['Перепад на фильтре', Tagtable.objects.filter(tagname='MEASURES\PDI_725')[0].tagindex])
    tag_list.append(['Перепад на дымососе', Tagtable.objects.filter(tagname='MEASURES\PDI_729')[0].tagindex])
    tag_list.append(['Разяряжение в гор. газоходе', Tagtable.objects.filter(tagname='MEASURES\PI_702')[0].tagindex])
    tag_list.append(['Частота ПЧ дымососа', Tagtable.objects.filter(tagname='MEASURES\SI_U721')[0].tagindex])

    for tag in tag_list:
        tag.append(Floattable.objects.filter(tagindex=tag[1]).order_by('-dateandtime')[0].val)

    #горелка
    power_sp = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\HY_F710')[0].tagindex).order_by('-dateandtime')[0].val
    gas_flow = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_810B')[0].tagindex).order_by('-dateandtime')[0].val
    air_flow = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_810C')[0].tagindex).order_by('-dateandtime')[0].val
    o2_flow =  Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\O2Flow')[0].tagindex).order_by('-dateandtime')[0].val
    alpha = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\Alpha')[0].tagindex).order_by('-dateandtime')[0].val
    lambd = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\Lambda')[0].tagindex).order_by('-dateandtime')[0].val
    standby = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='GENERAL\F711_LOCK')[0].tagindex).order_by('-dateandtime')[0].val
    power_mode = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='IO\HS1_F711')[0].tagindex).order_by('-dateandtime')[0].val

    #горячий газоход
    hotflue_p = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PI_702')[0].tagindex).order_by('-dateandtime')[0].val
    hotflue_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_705A')[0].tagindex).order_by('-dateandtime')[0].val

    #фильтр
    filter_dp = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PDI_725')[0].tagindex).order_by('-dateandtime')[0].val 
    t_before_filter = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_708')[0].tagindex).order_by('-dateandtime')[0].val
    #дымосос
    exhauster_dp = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PDI_729')[0].tagindex).order_by('-dateandtime')[0].val
    exhauster_pc = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SI_U721')[0].tagindex).order_by('-dateandtime')[0].val

    #дроссели
    hot_flue_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\PY_702')[0].tagindex).order_by('-dateandtime')[0].val
    over_door_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\ZI_704')[0].tagindex).order_by('-dateandtime')[0].val
    exhauster_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\ZI_706')[0].tagindex).order_by('-dateandtime')[0].val
    round_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\\xvi_v_cech')[0].tagindex).order_by('-dateandtime')[0].val
    filter3_gate = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\XVI_708')[0].tagindex).order_by('-dateandtime')[0].val
    drain_gate = "открыт" if not Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='VALVES\XV702_ZL')[0].tagindex).order_by('-dateandtime')[0].val else "закрыт"

    #дельта
    over_door_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_711Y')[0].tagindex).order_by('-dateandtime')[0].val
    cold_air_t = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\TI_711X')[0].tagindex).order_by('-dateandtime')[0].val
    deltaT = over_door_t - cold_air_t

    #печь
    furnace_rotation = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SY_KL711')[0].tagindex).order_by('-dateandtime')[0].val
    furnace_current = Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='MEASURES\SI_KL711')[0].tagindex).order_by('-dateandtime')[0].val
    loading_door_half = "открыта" if Floattable.objects.filter(tagindex=Tagtable.objects.filter(tagname='VALVES\XVF711P_ZL')[0].tagindex).order_by('-dateandtime')[0].val else "закрыта"
    
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
    step_time_remain = Automelt_info[0].step_time_remain
    deltat_stp = Automelt_info[0].deltat


    template = loader.get_template('FregatMonitoringApp/Furnace_info.html')
    context = {'furnace_num': 2,
               'power_sp': round(power_sp),
               'gas_flow': round(gas_flow),
               'air_flow': round(air_flow),
               'o2_flow': round(o2_flow),
               'alpha': round(alpha),
               'lambda': round(lambd,2),
               'standby': standby,
               'power_mode': power_mode,
               'filter_dp': round(filter_dp),
               't_before_filter': round(t_before_filter,1),
               'exhauster_dp': round(exhauster_dp),
               'hotflue_p': round(hotflue_p),
               'hotflue_t': round(hotflue_t,1),
               'exhauster_pc': round(exhauster_pc,1),
               'hot_flue_gate': round(hot_flue_gate),
               'over_door_gate': round(over_door_gate),
               'exhauster_gate': round(exhauster_gate),
               'round_gate': round(round_gate),
               'filter3_gate': round(filter3_gate),
               'drain_gate': drain_gate,    
               'over_door_t': round(over_door_t),
               'cold_air_t': round(cold_air_t,1),
               'deltaT': round(deltaT,1),
               'furnace_rotation': round(furnace_rotation, 1),
               'furnace_current': round(furnace_current,1),
               'loading_door_half': loading_door_half,
               'auto_mode': auto_mode,
               'melt_type' : melt_type,
               'melt_step' : melt_step,
               'step_total_time' : step_total_time,
               'step_time_remain' : step_time_remain,
               'deltat_stp' : deltat_stp,
               'shzm_position': shzm_position,
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
from django import template
from django.db.models.query_utils import subclasses
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context, loader
from django.urls import reverse

from .models import Floattable, Tagtable
from .models import Melttypes, Meltsteps, Substeps

def index(request):
    template = loader.get_template('FregatMonitoringApp/base.html')
    context = None
    return HttpResponse(template.render(context, request))

def error_message(request):
    template = loader.get_template('FregatMonitoringApp/ErrorMessage.html')
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

    template = loader.get_template('FregatMonitoringApp/furnace_info.html')
    context = {'tags_values': tag_list}

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

    template = loader.get_template('FregatMonitoringApp/Furnace_info.html')
    context = {'tags_values': tag_list}

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
    context=None
    return HttpResponse(template.render(context, request))

def AutoMeltsSaveSettings(request, meltID_1, meltID_2):
    
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
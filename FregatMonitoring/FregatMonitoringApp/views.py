from django import template
from django.http import HttpResponse
from django.template import loader

from .models import Floattable, Tagtable

def index(request):
    template = loader.get_template('FregatMonitoringApp/base.html')

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
    tag_dict = {'tags_values': tag_list}
    context = tag_dict

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
    tag_dict = {'tags_values': tag_list}
    context = tag_dict

    return HttpResponse(template.render(context, request))
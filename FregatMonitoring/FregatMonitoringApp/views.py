from django.http import HttpResponse

from .models import Floattable, Tagtable

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def Furnace_1_power(request):
    tag = Tagtable.objects.filter(tagname='MEASURES\HY_F711')
    last_value = Floattable.objects.filter(tagindex=tag[0].tagindex).order_by('-dateandtime')[:1]
    return HttpResponse('Задание мощности печь №1: %s ' % last_value[0].val)
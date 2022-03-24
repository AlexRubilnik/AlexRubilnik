from FregatMonitoringApp.models import Meltsteps
from django import template

register = template.Library()

@register.inclusion_tag('FregatMonitoringApp/include_templates/steps_templates.html', name='get_substebs_by_step')
def substebs_by_step(cur_melt_name: str, current_step: Meltsteps, furnace_substep: list):
    """ Выбирает подшаги из заданного списка, относящиеся к заданному шагу 

        input: 
               cur_melt_name - имя заданной плавки
               current_step - заданный шаг
               furnace_substeps - список пошагов
    """
    
    return {'melt_name': cur_melt_name, 'step': current_step, 'substeps': furnace_substep}

 
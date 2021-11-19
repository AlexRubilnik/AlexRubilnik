from django.contrib import admin

admin.site.disable_action('delete_selected')

from .models import Melttypes
from .models import Meltsteps
from .models import Substeps

class SubStepsInline(admin.TabularInline):
    model = Substeps
    show_change_link = True

class MeltStepsAdmin(admin.ModelAdmin):
    list_display = ['step_name', 'step_num']
    readonly_fields = ['step_name', 'step_num']
    inlines = [SubStepsInline] 

class MeltStepsInline(admin.TabularInline):
    model = Meltsteps
    exclude = ['cur_step_time']
    readonly_fields = ('step_name','step_num')
    can_delete = False
    show_change_link = True
    extra = 0

class MeltTypesAdmin(admin.ModelAdmin):
    list_display = ['melt_num', 'melt_furnace','melt_name']
    list_filter = ['melt_furnace']
    ordering = ['melt_num', 'melt_furnace']
    readonly_fields = ('melt_num', 'melt_furnace','melt_name')
    inlines = [MeltStepsInline] 

admin.site.register(Melttypes, MeltTypesAdmin)
admin.site.register(Meltsteps, MeltStepsAdmin )
#admin.site.register(Substeps)
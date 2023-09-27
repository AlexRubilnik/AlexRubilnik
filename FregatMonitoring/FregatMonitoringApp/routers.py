class FregatMonitoringAppRouter:
    """Роутер для определения, какой БД пользоваться приложению, и в каких случаях"""

    def db_for_read(self, model, **hints):
        if model._meta.db_table in ('AutoMelts','Avtoplavka_status','Avtoplavka_setpoints','Autoplavka_log','FloatTable','TagTable','MeltTypes',
                                    'MeltSteps','SubSteps','DailyGasesConsumption','GasesConsumptionsPerDay', 'Rarefaction_P2', 'Furnace1_errors_log', 
                                    'Furnace2_errors_log'):
            return 'production_fx'
        elif model._meta.db_table in ('Zebra',):
            return 'zebra'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.db_table in ('AutoMelts','Avtoplavka_setpoints','FloatTable','MeltTypes','MeltSteps','SubSteps'):
            return 'production_fx'
        return 'default'

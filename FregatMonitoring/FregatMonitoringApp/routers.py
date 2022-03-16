class FregatMonitoringAppRouter:
    """Роутер для определения, какой БД пользоваться приложению, и в каких случаях"""

    def db_for_read(self, model, **hints):
        if model._meta.db_table in ('AutoMelts','FloatTable','TagTable','MeltTypes','MeltSteps','SubSteps','DailyGasesConsumption','GasesConsumptionsPerDay'):
            return 'production_fx'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.db_table in ('AutoMelts','FloatTable','MeltTypes','MeltSteps','SubSteps'):
            return 'production_fx'
        return 'default'

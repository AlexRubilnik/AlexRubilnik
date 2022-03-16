# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Daily_gases_consumption(models.Model):
    id = models.SmallIntegerField(db_column='Id', primary_key=True)
    data = models.DateField(db_column='Data', blank=False, null=False)
    daily_consumption = models.FloatField(db_column='Daily_consumption', blank=False, null=True)
    gasname = models.CharField(db_column='GasName', blank=False, null=False, max_length=20)

    class Meta:
        managed = False
        db_table = 'DailyGasesConsumption'

class Gases_consumptions_per_day(models.Model): #Модель для извлечения почасовых расходов газов за определённый период
    id = models.SmallIntegerField(primary_key=True)
    data = models.SmallIntegerField(blank=True, null=True)#номер часа, за который посчитан расход. Например, если расход вычислен за сутки, то в этом поле будут номера от 1 до 23
    consumption = models.FloatField(blank=True, null=True)
    gasname = models.CharField(blank=True, null=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'GasesConsumptionsPerDay' #Такой таблицы в БД нет. Это нужно чтобы работал router на эту БД для этой модели



class Automelts(models.Model):
    furnace_no = models.SmallIntegerField(db_column='Furnace_No', primary_key=True)  # Field name made lowercase.
    auto_mode = models.BooleanField(db_column='Auto_mode', blank=True, null=True)  # Field name made lowercase.
    melt_type = models.SmallIntegerField(db_column='Melt_type', blank=True, null=True)  # Соответствует melt_num в Melttypes(вместе с furnace_no определяет плавку однозначно)
    melt_step = models.SmallIntegerField(db_column='Melt_step', blank=True, null=True)  # соответствует step_num в Meltsteps
    step_total_time = models.IntegerField(db_column='Step_total_time', blank=True, null=True)  # Field name made lowercase.
    step_time_remain = models.SmallIntegerField(db_column='Step_time_remain', blank=True, null=True)  # Field name made lowercase.
    deltat = models.SmallIntegerField(db_column='DeltaT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AutoMelts'

class Melts(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    meltno = models.IntegerField(db_column='MeltNo')  # Field name made lowercase.
    furnace = models.SmallIntegerField(db_column='Furnace')  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    pasta = models.FloatField(db_column='Pasta', blank=True, null=True)  # Field name made lowercase.
    coal = models.FloatField(db_column='Coal', blank=True, null=True)  # Field name made lowercase.
    soda = models.FloatField(db_column='Soda', blank=True, null=True)  # Field name made lowercase.
    iron = models.FloatField(db_column='Iron', blank=True, null=True)  # Field name made lowercase.
    dust = models.FloatField(db_column='Dust', blank=True, null=True)  # Field name made lowercase.
    oxides = models.FloatField(db_column='Oxides', blank=True, null=True)  # Field name made lowercase.
    slurry = models.FloatField(db_column='Slurry', blank=True, null=True)  # Field name made lowercase.
    fraction = models.FloatField(db_column='Fraction', blank=True, null=True)  # Field name made lowercase.
    pbmat = models.FloatField(db_column='PBMat', blank=True, null=True)  # Field name made lowercase.
    startmelt = models.DateTimeField(db_column='StartMelt', blank=True, null=True)  # Field name made lowercase.
    endmelt = models.DateTimeField(db_column='EndMelt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Melts'

class Rarefaction(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rf_in_furnace = models.FloatField(db_column='Rf_in_furnace', blank=True, null=True)  # Field name made lowercase.
    rf_in_ciclone_2pech = models.FloatField(db_column='Rf_in_ciclone_2pech', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TimeStamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Rarefaction'

class Tagtable(models.Model):
    tagname = models.CharField(db_column='TagName', max_length=255)  # Field name made lowercase.
    tagindex = models.SmallIntegerField(db_column='TagIndex', primary_key=True)  # Field name made lowercase.
    tagtype = models.SmallIntegerField(db_column='TagType')  # Field name made lowercase.
    tagdatatype = models.SmallIntegerField(db_column='TagDataType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TagTable'

    def __str__(self):
        return self.tagname

class Floattable(models.Model):
    dateandtime = models.DateTimeField(db_column='DateAndTime')  # Field name made lowercase.
    millitm = models.SmallIntegerField(db_column='Millitm')  # Field name made lowercase.
    tagindex = models.SmallIntegerField(db_column='TagIndex', primary_key=True)  # Field name made lowercase.
    val = models.FloatField(db_column='Val')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    marker = models.CharField(db_column='Marker', max_length=1, blank=True, null=True)  # Field name made lowercase.

    #tagindex_FK = models.ForeignKey(Tagtable, on_delete=models.CASCADE, hidden=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FloatTable'

    def __str__(self):
        return str(self.tagindex) + '=' + str(self.val)     

class Meltsteps(models.Model):
    melt = models.ForeignKey('Melttypes', models.DO_NOTHING, db_column='MELT_ID')  # IDплавки (по смыслу заключает в себе номер печи и номер плавки)
    step_id = models.AutoField(db_column='STEP_ID', primary_key=True)  # ID шага плавки
    step_num = models.SmallIntegerField(db_column='STEP_NUM')  # Номер шага плавки (совпадает с номером в шага ПЛК автоплавки)
    cur_step_time = models.SmallIntegerField(db_column='CUR_STEP_TIME', blank=True, null=True)  # Текущее время с начала выполнения шага
    step_name = models.CharField(db_column='STEP_NAME', max_length=20)  # Название шага

    class Meta:
        managed = False
        db_table = 'MeltSteps'

class Melttypes(models.Model):
    melt_id = models.AutoField(db_column='MELT_ID', primary_key=True)  # IDплавки (нечётные - для 1 печи, чётные - тот же тип плавки, но для 2 печи)
    melt_num = models.SmallIntegerField(db_column='MELT_NUM')  # Номер плавки по порядку (соответствует номеру плавки в ПЛК, одинаков для обоих печей для одинаковых типов плавки)
    melt_furnace = models.SmallIntegerField(db_column='MELT_FURNACE')  # Номер печи, для которой эта плавка
    melt_name = models.CharField(db_column='MELT_NAME', max_length=50)  # Название плавки(одинаковый для обоих печей для одинаковых типов плавки)

    class Meta:
        managed = False
        db_table = 'MeltTypes'

class Substeps(models.Model):
    step = models.ForeignKey(Meltsteps, models.DO_NOTHING, db_column='STEP_ID')  # ID шага плавки 
    substep_id = models.AutoField(db_column='SUBSTEP_ID', primary_key=True)  # ID подшага
    sub_step_num = models.SmallIntegerField(db_column='SUB_STEP_NUM')  # Номер подшага для данного шага
    sub_step_time = models.SmallIntegerField(db_column='SUB_STEP_TIME')  # Время выполнения подшага
    power_sp = models.IntegerField(db_column='POWER_SP', blank=True, null=True)  # Уставка мощности
    rotation_sp = models.IntegerField(db_column='ROTATION_SP', blank=True, null=True)  # Уставка вращения
    hotgate_sp = models.IntegerField(db_column='HOTGATE_SP', blank=True, null=True)  # Уставка открытия гор. газохода
    alpha_sp = models.IntegerField(db_column='ALPHA_SP', blank=True, null=True)  # Уставка Alpha

    class Meta:
        managed = False
        db_table = 'SubSteps'

class AutoMeltsInfo(models.Model): #Класс для сериализатора данных о текущем состоянии автоплавок
    furnace_no = models.IntegerField(blank=True, null=True)
    auto_mode = models.CharField(max_length=7, blank=True, null=True, default='')
    melt_name = models.CharField(max_length=50, blank=True, null=True, default='')
    step_name = models.CharField(max_length=20, blank=True, null=True, default='')
    step_total_time = models.IntegerField(blank=True, null=True, default='')
    step_time_remain = models.IntegerField(blank=True, null=True, default='')
    deltat = models.FloatField(blank=True, null=True, default='')
    deltat_stp = models.IntegerField(blank=True, null=True, default='')


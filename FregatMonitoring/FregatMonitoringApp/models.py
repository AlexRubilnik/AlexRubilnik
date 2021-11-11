# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Automelts(models.Model):
    furnace_no = models.SmallIntegerField(db_column='Furnace_No', primary_key=True)  # Field name made lowercase.
    auto_mode = models.BooleanField(db_column='Auto_mode', blank=True, null=True)  # Field name made lowercase.
    melt_type = models.SmallIntegerField(db_column='Melt_type', blank=True, null=True)  # Field name made lowercase.
    melt_step = models.SmallIntegerField(db_column='Melt_step', blank=True, null=True)  # Field name made lowercase.
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

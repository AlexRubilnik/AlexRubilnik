from django.db.models import fields
from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import Automelts, Floattable, Tagtable, Melttypes, AutoMeltsInfo

class FloattableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floattable
        fields = ['dateandtime', 'tagindex', 'val']

class MelttypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Melttypes
        fields = ['melt_num', 'melt_furnace', 'melt_name']

class AutomeltsSerializer(serializers.Serializer):

    furnace_no = serializers.IntegerField()
    auto_mode = serializers.CharField(max_length=7)
    melt_name = serializers.CharField(max_length=50)
    step_name = serializers.CharField(max_length=20)
    step_total_time = serializers.IntegerField()
    step_time_remain = serializers.IntegerField()
    deltat = serializers.FloatField()
    deltat_stp = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return AutoMeltsInfo.objects.create(**validated_data)



"""class FurnaceBaseTrendsSerializer(serializers.Serialize):
    name = serializers.CharField(max_length=100)
    values = {**}
"""
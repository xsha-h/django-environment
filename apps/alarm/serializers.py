from rest_framework import serializers

from alarm.models import AlarmType, AlarmLevel, Alarm


class AlarmTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlarmType
        fields = "__all__"


class AlarmLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlarmLevel
        fields = "__all__"


class AlarmSerializer(serializers.ModelSerializer):
    alarm_type = AlarmTypeSerializer()
    alarm_level = AlarmLevelSerializer()

    class Meta:
        model = Alarm
        fields = "__all__"


class DealAlarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alarm
        fields = ("id", )

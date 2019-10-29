from rest_framework import serializers

from accessControls.models import Accesses


class AccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accesses
        fields = "__all__"


class AddAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accesses
        fields = ("id", "username", "follow_users", "follow_nums",
                  "detail", "start_time", "end_time")


class UpdateAccessSerializer(serializers.ModelSerializer):
    # 审批人
    # username = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Accesses
        fields = ("feedback", )


class AccessCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accesses
        fields = "__all__"

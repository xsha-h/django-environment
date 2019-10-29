from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from logs.models import Logs


class LogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Logs
        fields = "__all__"

        # 在API页面中对字段的约束
        extra_kwargs = {
            "addtime": {"required": False, "read_only": True},
            "user_id": {"required": False, "read_only": True},
        }

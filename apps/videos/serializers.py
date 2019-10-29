from rest_framework import serializers

from videos.models import Videos


class MonitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Videos
        fields = ("name", "address",)


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = "__all__"

        # 在API页面中对字段的约束
        extra_kwargs = {
            "addtime": {"required": False, "read_only": True}
        }


class DeleteVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ("id", )

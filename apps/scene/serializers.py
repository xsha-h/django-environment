from rest_framework import serializers

from scene.models import Scene, Display


class SceneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scene
        exclude = ("level", )


class UpdateSceneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scene
        fields = ("code", )


class DisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Display
        fields = ("id", "content")

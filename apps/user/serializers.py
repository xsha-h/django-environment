from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = UserInfo
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    user1 = UserInfoSerializer(many=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"required": False}
        }


class AddUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ("account", )
        extra_kwargs = {
            "user_id": {"required": False}
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ("id", )

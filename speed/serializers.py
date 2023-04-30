from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import SpeedLimit, UserInfo, Vehicle, Penalty

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('auth_token',)

    def get_auth_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key
    
class SpeedLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model=SpeedLimit
        fields=('__all__')

class UserInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields= ('__all__')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=('__all__')

class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model=Penalty
        exclude=('id','user')

class PostPenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model=Penalty
        fields=('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=('password',)

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        exclude=('user',)

class PostVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=('__all__')


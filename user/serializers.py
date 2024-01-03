from .models import UserProfile
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        __module__ = UserProfile
        fields = '__all__'

    
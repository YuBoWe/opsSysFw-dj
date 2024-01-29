from .models import UserProfile
from rest_framework.serializers import ModelSerializer
import re
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, ContentType, Group, Permission


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PermSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'content_type': {'read_only': True},
            'codename': {'read_only': True},
        }
    content_type = ContentTypeSerializer(read_only=True)


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        # fields = '__all__'
        fields = [
            'id', 'username', 'password', 'phone', 'is_active', 'is_superuser', 'email'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'max_length': 14, 'min_length': 4},
            'is_active': {'default': False},
            'is_superuser': {'default': False},
        }

    ## 设置密码校验
    def validate_password(self, data):
        # 这里的data是明文
        # 密码规则：包含至少一个大写字母、一个小写字母、一个数字、一个特殊字符，且长度在6到20之间
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,16}$'

        if 6 <= len(data) <= 16:
            if re.match(pattern, data):
                return make_password(data)
            else:
                raise ValidationError('请设置强密码：包含至少一个大写字母、一个小写字母、一个数字、一个特殊字符')
        else:
            raise ValidationError('密码长度应该在6到16位之间')


print("=" * 30)
print(UserSerializer())

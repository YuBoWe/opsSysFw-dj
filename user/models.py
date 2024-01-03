from django.db import models
from django.contrib.auth.models import User, AbstractUser


class UserProfile(AbstractUser):
    class Meta:
        db_table = "auth_user"  # user_userprofile
        verbose_name = "用户详情信息表"
    phone = models.CharField(max_length=32, verbose_name="电话号码", blank=True, null=True)


"""oo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# 发token类
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

tov = TokenObtainPairView.as_view()

from user.views import oo_login

urlpatterns = [
    path('login/', tov),
    path('api/token/', tov, name='token_obtain_pair'),  # 要用户名和密码
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', oo_login)
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view


@api_view(['get', 'post'])
def oo_login(request: Request):
    # u = request.POST.get('username')
    # p = request.POST.get('password')
    # user = authenticate(username=u, password=p)
    # if user:  # session无关
    #     # 发令牌token sessionid
    #     login(request, user)  # request对象和user建立关联
    #     return HttpResponse('登录成功')
    # else:
    #     pass
    print("=" * 30)
    print(request.method, request._request.COOKIES, request.headers)
    print(request.data)
    print(request.user, bool(request.user), request.user.is_authenticated)
    print(request.auth, '~~~~~')  # None不成功
    print("=" * 30)
    # if request.auth:
    #     return Response({'view': 'login'})
    # else:
    #     return HttpResponseForbidden()
    return Response({'view': 'login post'})

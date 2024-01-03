from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from utils.exception import NotFound
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.views import APIView
from django.contrib.auth.models import User, AnonymousUser


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class MenuItem(dict):
    def __init__(self, id, name, path=None):
        super().__init__()
        self['id'] = id
        self['path'] = path
        self['name'] = name
        self['children'] = []

    def append(self, item):
        # self.children.append(item)
        self['children'].append(item)
        return self

    def extend(self, *items):
        self['children'].extend(items)

    def __getattr__(self, item):
        return self[item]

@api_view(['get'])
# @permission_classes([IsAuthenticated])
@permission_classes([])  # 无权限要求
# @permission_classes([IsSuperUser])
def menulist_view(request: Request):
    # u = request.POST.get('username')
    # p = request.POST.get('password')
    # user = authenticate(username=u, password=p)
    # if user:  # session无关
    #     # 发令牌token sessionid
    #     login(request, user)  # request对象和user建立关联
    #     return HttpResponse('登录成功')
    # else:
    #     pass
    # print("=" * 30)
    # print(request.method, request._request.COOKIES, request.headers)
    # print(request.data)
    # print(request.user, bool(request.user), request.user.is_authenticated)
    # print(request.auth, '~~~~~')  # None不成功
    # print("=" * 30)
    # if request.auth:
    #     return Response({'view': 'login'})
    # else:
    #     return HttpResponseForbidden()
    menulist = []
    # if request.user.is_superuser:
    if request.user:

        i1 = MenuItem(1, '用户管理')
        i2 = MenuItem(11, '用户列表', '/users')
        i3 = MenuItem(12, '角色列表', '/users/roles')
        i4 = MenuItem(13, '权限列表', '/user/perms')
        # i1.append(i2).append(i3).append(i4)
        i1.extend(i2, i3, i4)
        menulist.append(i1)

    i5 = MenuItem(2, 'xx管理')
    i6 = MenuItem(21, 'xx列表', '/cmbd')
    i5.extend(i6)
    menulist.append(i5)

    return Response({
        'default': '11',
        'menulist': menulist
    })


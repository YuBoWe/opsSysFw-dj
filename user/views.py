from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, ContentType, Group, Permission

from utils.exception import NotFound
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, DjangoModelPermissions
from rest_framework.views import APIView
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import UserProfile
from .serializers import UserSerializer, PermSerializer, GroupSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model
from utils.exception import InvalidPassword


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


_exclude_contenttypes = [
    c.id for c in ContentType.objects.filter(model__in=[
        'logentry', 'group', 'permission', 'contenttype', 'session'
    ])
]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    search_fields = ['name']

    @action(['GET'], detail=True)
    def perms(self, request, pk):
        obj = self.get_object()
        data = GroupSerializer(obj).data
        data['allPerms'] = list(PermViewSet.queryset.values('id', 'name'))
        return Response(data)


class PermViewSet(ModelViewSet):
    queryset = Permission.objects.exclude(content_type__in=_exclude_contenttypes)
    serializer_class = PermSerializer
    search_fields = ['name']


class UserViewSet(ModelViewSet):
    # queryset = UserProfile.objects.all()
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']
    search_fields = ['username', 'email']

    # 详情页禁止修改username，如果提供用户名，它就要验证用户名唯一性，且尝试修改用户名
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('username', None)
        request.data.pop('password', None)
        request.data.pop('id', None)
        request.data.pop('is_superuser', None)
        return super().partial_update(request, *args, **kwargs)

    def get_object(self):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == 1 or pk == '1':
                raise Http404
        return super().get_object()

    @action(['GET'], detail=True)
    def roles(self, request, pk):
        user = self.get_object()
        data = UserSerializer(instance=user).data
        data['roles'] = [p.get('id') for p in user.groups.values('id')]
        data['roleList'] = Group.objects.values('id', 'name')
        return Response(data)

    @roles.mapping.patch
    def setRoles(self, request, pk):
        user = self.get_object()
        user.groups.set(request.data.get('group_list'))
        return Response()

    @action(['GET'], detail=False, url_path='whoami', permission_classes=[IsAuthenticated])
    def whoami(self, request):
        return Response({
            'currentUser': {'username': request.user.username, 'id': request.user.id}
        })

    # 验证修改密码
    @action(['POST'], detail=False)
    def myselfChpwd(self, request):
        user: UserProfile = request.user
        # print(user.is_superuser, user.password, user.username, user.id)
        serializer = UserSerializer(instance=user)
        if UserSerializer.validate_password(serializer, data=request.data['password']):
            if user.check_password(request.data['oldPassword']):
                # print(user.password)
                user.set_password(request.data['password'])
                # print(user.password)
                user.save()
                return Response()
            else:
                raise InvalidPassword

    # 管理员修改用户密码
    @action(['POST'], detail=True, permission_classes=[IsSuperUser])
    def adChpwd(self, request, pk=None):
        # print(pk)
        user = self.get_object()
        serializer = UserSerializer(instance=user)
        if UserSerializer.validate_password(serializer, data=request.data['password']):
            if user.check_password(request.data['oldPassword']):
                user.set_password(request.data['password'])
                user.save()
                return Response()
            else:
                raise InvalidPassword


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
@permission_classes([IsAuthenticated])
# @permission_classes([])  # 无权限要求
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
    if request.user.is_superuser:

        i1 = MenuItem(1, '用户管理')
        i2 = MenuItem(11, '用户列表', '/users')
        i3 = MenuItem(12, '角色列表', '/users/roles')
        i4 = MenuItem(13, '权限列表', '/users/perms')
        # i1.append(i2).append(i3).append(i4)
        i1.extend(i2, i3, i4)
        menulist.append(i1)

    i5 = MenuItem(2, '测试')
    i6 = MenuItem(21, 'slot', '/TS')
    i5.extend(i6)
    menulist.append(i5)

    return Response({
        'default': '11',
        'menulist': menulist
    })


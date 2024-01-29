from django.urls import path
from .views import menulist_view, UserViewSet, PermViewSet, GroupViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('mgr', UserViewSet)  # /users/mgr /users/mgr/100
router.register('perms', PermViewSet)
router.register('roles', GroupViewSet)  # /users/roles /users/roles/1

# users
urlpatterns = [
    path('menulist/', menulist_view),  # /users/menulist
] + router.urls

from django.urls import path
from .views import menulist_view, UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', UserViewSet)
# users
urlpatterns = [
    path('menulist/', menulist_view),  # /users/menulist
] + router.urls

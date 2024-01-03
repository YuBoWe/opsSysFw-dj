from django.urls import path
from .views import menulist_view

# users
urlpatterns = [
    path('menulist/', menulist_view),  # /users/menulist
]

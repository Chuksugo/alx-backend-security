from django.urls import path
from . import views

urlpatterns = [
    path("login/anon/", views.anonymous_login, name="anonymous_login"),
    path("login/user/", views.user_login, name="user_login"),
]

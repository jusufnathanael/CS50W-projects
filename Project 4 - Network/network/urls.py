
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_or_edit", views.add_or_edit, name="add_or_edit"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("like/<int:id>", views.like, name="like"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

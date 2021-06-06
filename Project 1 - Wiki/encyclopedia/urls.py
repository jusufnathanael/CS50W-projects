from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("wiki/<str:name>", views.page, name="page"),
    path("search/", views.search, name="search"),
    path("wiki/<str:name>/edit", views.edit, name="edit"),
    path("random", views.rand, name="random")
]

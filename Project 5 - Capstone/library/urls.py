from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("book/<int:id>", views.book, name="book"),
    path("account/<str:name>", views.account, name="account"),

    # ACTIONS
    path("borrow/<int:id>", views.borrow, name="borrow"),
    path("reserve/<int:id>", views.reserve, name="reserve"),
    path("cancel/<int:id>", views.cancel, name="cancel"),
    path("retturn/<int:id>", views.retturn, name="retturn"),
    path("pay", views.pay, name="pay"),
    path("review/<int:id>", views.review, name="review"),

    # AUTHENTICATION
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]

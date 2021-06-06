from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/close", views.close, name="close"),
    path("category/", views.category, name="category"),
    path("category/<str:name>", views.filtered, name="filtered"),
    
    path("add", views.add, name="add"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("comment/<int:id>", views.comment, name="comment"),

    path("watchlist/", views.show_watchlist, name="show_watchlist"),
    path("watchlist/add/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove/<int:id>", views.remove_watchlist, name="remove_watchlist"),
]

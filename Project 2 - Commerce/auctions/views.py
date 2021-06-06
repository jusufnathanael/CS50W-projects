from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.db.models.fields import DateTimeField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import *


def index(request):
    items = Listing.objects.filter(active=True)
    max_prices = []
    for item in items:
        max_price = Bid.objects.filter(item=item).aggregate(Max('price')).get('price__max')
        if max_price:
            max_prices += [max_price]
        else:
            max_prices += [item.price]
    return render(request, "auctions/index.html", {
        "listings": zip(items, max_prices)
    })


def listing(request, id):
    if "username" in request.session:
        user = User.objects.get(username=request.session["username"])
    else:
        user = None
    item = Listing.objects.get(id=id)
    if WatchList.objects.filter(user=user, item=item):
        watched = True
    else:
        watched = False
    max_price = Bid.objects.filter(item=item).aggregate(Max('price')).get('price__max')
    if max_price:
        highest_bid = Bid.objects.get(item=item, price=max_price)
    else:
        highest_bid = None
    no_of_bid = Bid.objects.filter(item=item).count()
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=id),
        "watched": watched, "user": user,
        "comments": Comment.objects.filter(item=item).order_by('-date'),
        "max_bid": highest_bid, "count": no_of_bid
    })


@login_required
def close(request, id):
    user = User.objects.get(username=request.session["username"])
    listing = Listing.objects.get(id=id)
    if listing.user == user:
        listing.active = False
        listing.closed_date = datetime.utcnow()
        listing.save(update_fields=['active', 'closed_date'])
        watchlists = WatchList.objects.filter(item=listing)
        watchlists.delete()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def category(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all().order_by('name')
    })


def filtered(request, name):
    category = Category.objects.get(name=name)
    return render(request, "auctions/filtered.html", {
        "category": category,
        "listings": Listing.objects.filter(active=True, category=category)
    })


@login_required
def add(request):

    def is_valid(request):
        params = ["name", "price", "description"]
        for param in params:
            if not request.POST[param]:
                return False
        return True

    if request.method == "POST":
        user = User.objects.get(username=request.session["username"])
        name = request.POST["name"]
        price = request.POST["price"]
        if request.POST["category"]:
            category = Category.objects.get(name=request.POST["category"])
        else:
            category = None
        image_url = request.POST["image_url"]
        description = request.POST["description"]
        if not is_valid(request):
            return render(request, "auctions/add.html", {
                "name": name, "price": price, "image_url": image_url, "description": description,
                "selected": category, "categories": Category.objects.all().order_by('name'),
            })
        listing = Listing(name=name, price=price, category=category, image_url=image_url, description=description, user=user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/add.html", {
        "categories": Category.objects.all().order_by('name'),
    })


@login_required
def bid(request, id):

    def is_valid(request, item):
        current_price = float(request.POST["price"])
        max_price = Bid.objects.filter(item=item).aggregate(Max('price')).get('price__max')
        start_price = item.price
        if current_price >= start_price and (not max_price or current_price > float(max_price)):
            return True
        return False

    user = User.objects.get(username=request.session["username"])
    item = Listing.objects.get(id=id)
    if request.method == "POST" and request.POST["price"] and is_valid(request, item):
        price = request.POST["price"]
        bid = Bid(user=user, item=item, price=price)
        bid.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def comment(request, id):
    user = User.objects.get(username=request.session["username"])
    details = request.POST["comment"]
    comment = Comment(user=user, item=Listing.objects.get(id=id), details=details)
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def show_watchlist(request):
    user = User.objects.get(username=request.session["username"])
    watchlists = WatchList.objects.filter(user=user)
    max_prices = []
    for watchlist in watchlists:
        max_price = Bid.objects.filter(item=watchlist.item).aggregate(Max('price')).get('price__max')
        if max_price:
            max_prices += [max_price]
        else:
            max_prices += [watchlist.item.price]
    return render(request, "auctions/watchlist.html", {
        "watchlists": zip(watchlists, max_prices)
    })


@login_required
def add_watchlist(request, id):
    user = User.objects.get(username=request.session["username"])
    watchlist = WatchList(user=user, item=Listing.objects.get(id=id))
    watchlist.save()
    return HttpResponseRedirect(reverse("show_watchlist"))


@login_required
def remove_watchlist(request, id):
    user = User.objects.get(username=request.session["username"])
    watchlist = WatchList.objects.get(user=user, item=Listing.objects.get(id=id))
    watchlist.delete()
    return HttpResponseRedirect(reverse("show_watchlist"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session["username"] = username
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    if "username" in request.session:
        del request.session["username"]
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        request.session["username"] = username
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

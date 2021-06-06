import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.db.models.fields import IntegerField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Avg, F, Sum, DateTimeField, ExpressionWrapper
from django.db.models.functions import Now
from datetime import timedelta, datetime, date
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import *

# Create your views here.
@login_required
def index(request):
    books = Book.objects.all()
    # search filter
    search = False
    title = year = category = author = ''
    if 'qt' in request.GET and request.GET['qt']:
        books = books.filter(title__icontains=request.GET['qt'])
        title = request.GET['qt']
    if 'qy' in request.GET and request.GET['qy']:
        min_date = datetime.strptime(f"{request.GET['qy']}-01-01", "%Y-%m-%d")
        max_date = datetime.strptime(f"{request.GET['qy']}-12-31", "%Y-%m-%d")
        books = books.filter(published_date__gte=min_date).filter(published_date__lte=max_date)
        year = request.GET['qy']
        search = True
    if 'qc' in request.GET and request.GET['qc']:
        books = books.filter(category=Category.objects.get(name=request.GET['qc']))
        category = request.GET['qc']
        search = True
    if 'qa' in request.GET and request.GET['qa']:
        books = books.filter(authors__icontains=request.GET['qa'])
        author = request.GET['qa']
        search = True
    # pagination
    paginator = Paginator(books, 20) # show 20 books per page
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    page_books = paginator.get_page(page_number)
    # check if the user is borrowing the book or not, and if cannot button disabled
    borrows = list(Borrow.objects.filter(user=request.user).values('book'))
    borrowed_books = [book['book'] for book in borrows]
    reserves = list(Reserve.objects.filter(user=request.user).values('book'))
    reserved_books = [book['book'] for book in reserves]
    has_unpaid_fines = False
    has_reached_maximum = False
    if Borrow.objects.filter(user=request.user, duedate__lt=datetime.now()).exists(): has_unpaid_fines = True
    if Borrow.objects.filter(user=request.user).count() >= 4: has_reached_maximum = True
    return render(request, "library/index.html", {
        "books": page_books,
        "allcategories": Category.objects.all(),
        "borrowed": borrowed_books, "reserved": reserved_books,
        "has_unpaid_fines": has_unpaid_fines, "has_reached_maximum": has_reached_maximum,
        "num_pages": range(paginator.num_pages), "current_page": int(page_number),
        "title": title, "year": year, "qcategory": category, "author": author, "search": search
    })


@login_required
def book(request, id):
    book = Book.objects.get(id=id)
    person_eq_user = False
    if book.status == "BORROWED":
        due_date = Borrow.objects.get(book=book).duedate
        if Borrow.objects.get(book=book).user == request.user: person_eq_user = True
    elif book.status == "RESERVED":
        due_date = Reserve.objects.get(book=book).duedate
        if Reserve.objects.get(book=book).user == request.user: person_eq_user = True
    else:
        due_date = None
    reviews = Review.objects.filter(book=Book.objects.get(id=id))
    num_rate = reviews.count()
    if num_rate > 10:
        rating = reviews.aggregate(Avg('rate'))
    else:
        rating = None
    my_rating = None
    if Review.objects.filter(book=Book.objects.get(id=id), user=request.user).exists():
        my_rating = Review.objects.get(book=Book.objects.get(id=id), user=request.user).rate
    has_unpaid_fines = False
    has_reached_maximum = False
    if Borrow.objects.filter(user=request.user, duedate__lt=datetime.now()).exists(): has_unpaid_fines = True
    if Borrow.objects.filter(user=request.user).count() >= 4: has_reached_maximum = True
    return render(request, "library/book.html", {
        "book": Book.objects.get(id=id),
        "due_date": due_date, "rating": rating,
        "person_eq_user": person_eq_user,
        "reviews": reviews, "my_rating": my_rating,
        "allcategories": Category.objects.all(),
        "has_unpaid_fines": has_unpaid_fines, "has_reached_maximum": has_reached_maximum
    })

@login_required
def review(request, id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("book", args=(id,)))
    data = json.loads(request.body)
    rate = data.get("id") if data.get("id") != 'None' else None
    Review.objects.create(user=request.user, book=Book.objects.get(id=id), rate=rate, details=data.get("details"))
    return HttpResponseRedirect(reverse("book", args=(id,)))



@login_required
def borrow(request, id):

    def is_available(request, id):
        # if book is not available and the user is not reserving it
        if Book.objects.get(id=id).status != "AVAILABLE" and \
            not (Book.objects.get(id=id).status == "RESERVED" and \
                Reserve.objects.filter(user=request.user, book=Book.objects.get(id=id)).exists()): return False
        # if the user has unpaid fines
        if Borrow.objects.filter(user=request.user, duedate__lt=datetime.now()).exists(): return False
        # if the user has reached the booking limits
        if Borrow.objects.filter(user=request.user).count() >= 4: return False
        return True

    if not is_available(request, id):
        return HttpResponseRedirect(reverse("index"))
    duedate = date.today() + timedelta(days=28)
    Borrow.objects.create(user=request.user, book=Book.objects.get(id=id), duedate=duedate)
    Book.objects.filter(id=id).update(status="BORROWED")
    reserve = Reserve.objects.filter(user=request.user, book=Book.objects.get(id=id))
    if reserve.exists(): reserve.delete()
    total = Borrow.objects.filter(user=request.user).count()
    return JsonResponse({"message": "Email sent successfully.", "total": total}, status=201)
    # return HttpResponseRedirect(reverse("account", args=(request.user.username,)))


@login_required
def reserve(request, id):

    def is_available(request, id):
        # if book is not under borrowed status
        if Book.objects.get(id=id).status != "BORROWED": return False
        # if the user is borrowing the book
        if Borrow.objects.filter(user=request.user, book=Book.objects.get(id=id)).exists(): return False
        # if the user has unpaid fines
        if Borrow.objects.filter(user=request.user, duedate__lt=datetime.now()).exists(): return False
        return True

    if not is_available(request, id):
        return HttpResponseRedirect(reverse("index"))
    Reserve.objects.create(user=request.user, book=Book.objects.get(id=id))
    Book.objects.filter(id=id).update(status="RESERVED")
    return HttpResponseRedirect(reverse("account", args=(request.user.username,)))


@login_required
def cancel(request, id):
    reservation = Reserve.objects.filter(user=request.user, book=Book.objects.get(id=id))
    if not reservation.exists():
        return HttpResponseRedirect(reverse("index"))
    reservation.delete()
    if Borrow.objects.filter(book=Book.objects.get(id=id)).exists():
        Book.objects.filter(id=id).update(status="BORROWED")
    else:
        Book.objects.filter(id=id).update(status="AVAILABLE")
    return HttpResponseRedirect(reverse("account", args=(request.user.username,)))


@login_required
def retturn(request, id):
    borrowing = Borrow.objects.filter(user=request.user, book=Book.objects.get(id=id))
    if not borrowing.exists():
        return HttpResponseRedirect(reverse("index"))
    if Borrow.objects.filter(user=request.user, book=Book.objects.get(id=id), duedate__lt=datetime.now()).exists():
        # unpaid fines
        return HttpResponseRedirect(reverse("index"))
    borrowing.delete()
    reservation = Reserve.objects.filter(book=Book.objects.get(id=id))
    if reservation.exists():
        duedate = duedate = date.today() + timedelta(days=14)
        reservation.update(duedate=duedate)
    else:
        Book.objects.filter(id=id).update(status="AVAILABLE")
    return HttpResponseRedirect(reverse("account", args=(request.user.username,)))


@login_required
def account(request, name):
    if request.user.username != name:
        return HttpResponseRedirect(reverse("index"))
    borrowings = Borrow.objects.filter(user=request.user)
    reservations = Reserve.objects.filter(user=request.user)
    payments = Borrow.objects.filter(user=request.user, duedate__lt=datetime.now())
    payments = payments.annotate(fine=ExpressionWrapper((Now()-F('duedate'))/86400/1000000, output_field=IntegerField()))
    return render(request, "library/account.html", {
        "borrowings": borrowings,
        "reservations": reservations,
        "payments": payments,
        "allcategories": Category.objects.all()
    })


def pay(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("account", args=(request.user.username,)))
    borrowings = Borrow.objects.filter(id__in=request.POST.getlist("checkbox"))
    Payment.objects.create(user=request.user, card=request.POST["card-number"], amount=request.POST["amount"])
    for borrowing in borrowings:
        reservation = Reserve.objects.filter(book=Book.objects.get(id=borrowing.book.id))
        if reservation.exists():
            Book.objects.filter(id=borrowing.book.id).update(status="BORROWED")
            duedate = duedate = date.today() + timedelta(days=14)
            reservation.update(duedate=duedate)
        else:
            Book.objects.filter(id=borrowing.book.id).update(status="AVAILABLE")
        borrowing.delete()
    return HttpResponseRedirect(reverse("account", args=(request.user.username,)))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
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
            return render(request, "library/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "library/login.html")


def logout_view(request):
    logout(request)
    if "username" in request.session:
        del request.session["username"]
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "library/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "library/register.html", {
                "message": "Username already taken."
            })
        request.session["username"] = username
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "library/register.html")

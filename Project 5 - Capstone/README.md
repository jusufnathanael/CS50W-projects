# Library

This web application is a library system that can manage book borrowing, returning and other related operations efficiently and effectively. This application is designed using Django.



### Distinctiveness and Complexity

This app has different concept and model compared to CS50 Project 2 Commerce and CS50 Project 4 Network. Since this app primarily manages book borrowings and reservations within the library, it is clearly not a social network app nor an e-commerce site.

1. This app has three entities (User, Book, and Category) and 4 relations (Borrow, Reserve, Payment, and Review), which sum to a total of 7 models.
2. The front-end utilizes Javascript and Bootstrap CSS to make the app more interactive and user-friendly.
3. The back-end utilizes Django and the default sqlite3 database.
4. Users can use the four functionalities within this app to borrow a book, reserve a book, pay a fine, and make a review to a book. The status of the book and these functionalities need to be adjusted accordingly depending on which account is using the app.
5. The index display is paginated to show only 20 books per page.



### Setup Guide

To run this app:

1. Make sure you have Python and Django installed to your local computer.
2. Run `python manage.py makemigrations` and `python manage.py migrate` to set up the database.
3. From the `capstone` directory, run `python manage.py runserver`.
4. You can also load the `.sql` files under the `data` directory that contain sample data.
5. Open your browser and visit from `http://127.0.0.1:8000/`.
6. Register a new account and you are ready to go!



### Rules and Conditions

- Users can borrow books for a period of 4 weeks if available and up to a maximum of 4 books.
- If a book is currently borrowed by a member, users can proceed to reserve the book instead.
- Users can also cancel a reservation at any time or convert the reservation to borrowing when the book becomes available.
- Any reservation will due 2 weeks after the book becomes available.
- Users can rate and leave a review for any books.
- The library charges a fine of $1 per book per day if the user fails to return a borrowed book on the stipulated due date.
- If the user has any unpaid fines, the user is not allowed to make any further borrowings or reservations until the fines are paid.
- Payment of fine can be made online with credit card.



### Functionalities

1. All books:
   - Users can view all books and the short details, limited to 20 books per page.
   - Users can immediately proceed to borrow or reserve any book if the situation allows by clicking the provided buttons.
2. My account:
   - Users can view all the borrowings, reservations, and fines (if any).
   - Users can also return the book and cancel any book reservation on this page.
3. Search:
   - Users can search for a book based on a title.
   - Advanced filter allows users to filter the search result based on category, year of publication, and the author.



### Files

***Python Files***

- admin.py: model registration for Django admin page.
- models.py: the models and fields exist within this app.
- urls.py: the URLs related to this app.
- views.py: functions containing multiple tasks that will run on the server, especially in relation to the database.

***HTML Files***

- layout.html: the general layout of the app.
- login.html: handles the account login view.
- register.html: handles the account registration view.
- index.html: displays the lists of all books, limited to 20 books per page.
- book.html: displays the details of each individual book.
- account.html: displays the borrowing, reservation, and payment status of the user.
- paginator.html: handles the pagination of index (included in the index.html).
- search.html: handles the search functionality of the app.

***Javascript Files***

- index.js: handles the various buttons on the index.html pages.
- book.js: handles the star-rating functionality of each individual book.
- account.js: handles the pagination functionality of the various tabs.

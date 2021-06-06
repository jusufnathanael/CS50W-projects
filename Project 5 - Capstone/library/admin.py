from django.contrib import admin

from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class BookAdmin(admin.ModelAdmin):
    pass

class BorrowAdmin(admin.ModelAdmin):
    pass

class ReserveAdmin(admin.ModelAdmin):
    pass

class PaymentAdmin(admin.ModelAdmin):
    pass

class ReviewAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Review, ReviewAdmin)
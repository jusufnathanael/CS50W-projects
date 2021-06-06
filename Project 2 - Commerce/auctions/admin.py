from django.contrib import admin

from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class ListingAdmin(admin.ModelAdmin):
    pass


class BidAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class WatchListAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WatchList, WatchListAdmin)
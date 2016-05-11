from django.contrib import admin
from OnlineLibraryApp.models import Category, Book, User, BookMark, BookCategory, Comment
# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(User)
admin.site.register(BookMark)
admin.site.register(BookCategory)
admin.site.register(Comment)
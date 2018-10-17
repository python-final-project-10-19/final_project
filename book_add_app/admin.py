from django.contrib import admin
from .models import Book

# admin.site.register(Book)


class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added', 'last_borrowed')


admin.site.register(Book, BookAdmin)

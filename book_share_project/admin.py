from django.contrib import admin
from book_share_project.models import Book, Profile, Notifications, Document

# admin.site.register(Book)


class BookAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


class NotificationsAdmin(admin.ModelAdmin):
    pass


class DocumentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(Document, DocumentAdmin)

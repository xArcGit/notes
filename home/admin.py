from django.contrib import admin
from .models import Notes, User


class NotesAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "shareid")  # Updated "createdAt" to "created"


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")


admin.site.register(Notes, NotesAdmin)
admin.site.register(User, UserAdmin)

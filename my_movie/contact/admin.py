from django.contrib import admin

from .models import Contact

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')
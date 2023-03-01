from django.contrib import admin
from .models import ClubAjedrez


@admin.register(ClubAjedrez)
class ClubAjedrezAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'president')
    list_filter = ('phone', 'address')
    search_fields = ('name', 'body')
    readonly_fields = ('created', 'updated')

from django.contrib import admin
from .models import Circular


@admin.register(Circular)
class Circulardmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author')
    list_filter = ('author', 'publish')
    search_fields = ('title', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-publish',)
    readonly_fields = ('created', 'updated', 'search_date')

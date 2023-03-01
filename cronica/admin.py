from django.contrib import admin
from .models import Cronica


@admin.register(Cronica)
class CronicaAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'torneo', 'author')
    list_filter = ('author', 'publish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-publish',)
    readonly_fields = ('created', 'updated')

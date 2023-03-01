from django.contrib import admin
from .models import TorneoDiputacion, RegistrationTournamentDiputacion


@admin.register(TorneoDiputacion)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'quantity', 'start', 'finish', 'location', 'province')
    list_filter = ('location', 'province', 'start', 'finish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    # ordering = ('-start',)
    readonly_fields = ('created', 'updated')


@admin.register(RegistrationTournamentDiputacion)
class TournamentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'surnames', 'mail', 'tournament_title', 'category', 'status', 'paid')
    list_filter = ('tournament_title', 'category', 'status', 'paid')

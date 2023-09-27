from .models import Pokemon, PokemonEntity
from django.contrib import admin


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ['title_ru']


@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ['pokemon', 'level', 'appeared_at', 'disappeared_at']


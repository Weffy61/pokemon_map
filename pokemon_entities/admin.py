from .models import Pokemon, PokemonEntity
from django.contrib import admin


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    pass

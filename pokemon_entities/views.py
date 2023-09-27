import folium
import json
from .models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render
from pogomap.settings import MEDIA_URL, MEDIA_ROOT
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        img_path = request.build_absolute_uri(f'{MEDIA_URL}{pokemon.image}')
        pokemon_img = img_path
        time_now = localtime()
        for pokemon_entity in pokemon_entities.filter(pokemon=pokemon,
                                                      appeared_at__lt=time_now,
                                                      disappeared_at__gt=time_now):
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon_img
            )

    pokemons_on_page = []

    for pokemon in pokemons:
        img_path = request.build_absolute_uri(f'{MEDIA_URL}{pokemon.image}')
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': img_path,
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()
    for pokemon in pokemons:
        if pokemon.pk == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities.filter(pokemon=requested_pokemon):
        img_path = request.build_absolute_uri(f'{MEDIA_URL}{pokemon_entity.pokemon.image}')
        pokemon = {
            "pokemon_id": pokemon_entity.pokemon.pk,
            "title_ru": pokemon_entity.pokemon.title,
            "img_url":  img_path,
            "entity":
            {
                "level": pokemon_entity.level,
                "lat": pokemon_entity.lat,
                "lon": pokemon_entity.lon,
            }
        }

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })

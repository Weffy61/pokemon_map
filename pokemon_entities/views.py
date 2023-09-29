import folium
from .models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render
from pogomap.settings import MEDIA_URL
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
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_now = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=time_now,
                                                    disappeared_at__gt=time_now)
    pokemons_on_page = []

    for pokemon_entity in pokemon_entities:
        pokemon_img_path = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        pokemons_on_page.append({
            'pokemon_id': pokemon_entity.pokemon.pk,
            'img_url': pokemon_img_path,
            'title_ru': pokemon_entity.pokemon.title_ru,
        })
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_img_path
        )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(pk=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    requested_pokemon = pokemon
    time_now = localtime()
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon,
                                                    appeared_at__lt=time_now,
                                                    disappeared_at__gt=time_now)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_img_path = request.build_absolute_uri(pokemon.image.url)
    pokemon = {
        "pokemon_id": requested_pokemon.pk,
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.descr,
        "img_url": pokemon_img_path,
        "entities": []
    }
    if requested_pokemon.previous_evolution:
        pokemon['previous_evolution'] = {
            "title_ru": requested_pokemon.previous_evolution.title_ru,
            "pokemon_id": requested_pokemon.previous_evolution.pk,
            "img_url": request.build_absolute_uri(requested_pokemon.previous_evolution.image.url)
        }
    try:
        if requested_pokemon.next_evolutions:
            pokemon['next_evolution'] = {
                "title_ru": requested_pokemon.next_evolutions.get().title_ru,
                "pokemon_id": requested_pokemon.next_evolutions.get().pk,
                "img_url": request.build_absolute_uri(requested_pokemon.next_evolutions.get().image.url)
            }
    except Pokemon.DoesNotExist:
        pass
    except Pokemon.MultipleObjectsReturned:
        pass

    for pokemon_entity in pokemon_entities:
        entity = {
            "level": pokemon_entity.level,
            "lat": pokemon_entity.lat,
            "lon": pokemon_entity.lon,
        }
        pokemon["entities"].append(entity)

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon['img_url']
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })

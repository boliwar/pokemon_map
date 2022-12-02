import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Pokemon, PokemonEntity
from pogomap.settings import MEDIA_URL

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
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    localtime = timezone.localtime()
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=localtime, disappeared_at__gt=localtime)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        filepath = request.build_absolute_uri(f'{MEDIA_URL}{pokemon.img}')
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': filepath,
            'title_ru': pokemon.title,
        })

        pokemon_objects = pokemon_entities.filter(pokemon=pokemon)
        for pokemon_object in pokemon_objects:
            add_pokemon(
                folium_map, pokemon_object.lat,
                pokemon_object.lon,
                filepath
            )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    localtime = timezone.localtime()
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    filepath = request.build_absolute_uri(f'{MEDIA_URL}{requested_pokemon.img}')

    pokemon_on_page = {'pokemon_id': requested_pokemon.id,
                       'img_url': filepath,
                       'title_ru': requested_pokemon.title,
                       'title_en': requested_pokemon.title_en,
                       'title_jp': requested_pokemon.title_jp,
                       'description': requested_pokemon.description,
                       }

    if requested_pokemon.previous_evolution:
        pokemon_on_page.setdefault('previous_evolution',
                                   {'pokemon_id': requested_pokemon.previous_evolution.id,
                                    'img_url': request.build_absolute_uri(f'{MEDIA_URL}{requested_pokemon.previous_evolution.img}'),
                                    'title_ru': requested_pokemon.previous_evolution.title,
                                   })

    try:
        next_pokemon = requested_pokemon.next_evolutions.all()
        if next_pokemon:
            pokemon_on_page.setdefault('next_evolution',
                                       {'pokemon_id': next_pokemon[0].id,
                                        'img_url': request.build_absolute_uri(f'{MEDIA_URL}{next_pokemon[0].img}'),
                                        'title_ru': next_pokemon[0].title,
                                        })

    except Pokemon.DoesNotExist:
        pass

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = requested_pokemon.pokemon_entities.filter(appeared_at__lte=localtime,
                                                               disappeared_at__gt=localtime)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            filepath
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })

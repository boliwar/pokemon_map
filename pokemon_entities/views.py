import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from .models import Pokemon, PokemonEntity


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
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']
    localtime = timezone.localtime()
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        filepath = request.build_absolute_uri(f'media/{pokemon.img}')
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': filepath,
            'title_ru': pokemon.title,
        })

        pokemon_entitys = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lte=localtime,
                                                       disappeared_at__gt=localtime)
        for pokemon_entity in pokemon_entitys:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                filepath
            )

    # for pokemon in pokemons:
    #     pokemons_on_page.append({
    #         'pokemon_id': pokemon.id,
    #         'img_url': pokemon.img,
    #         'title_ru': pokemon.title,
    #     })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']

    localtime = timezone.localtime()
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    filepath = request.build_absolute_uri(f'../../media/{requested_pokemon.img}')

    pokemon_on_page = {'pokemon_id': requested_pokemon.id,
                       'img_url': filepath,
                       'title_ru': requested_pokemon.title,
                       'title_en': requested_pokemon.title_en,
                       'title_jp': requested_pokemon.title_jp,
                       'description': requested_pokemon.description,
                       }

    try:
        preview_pokemon = Pokemon.objects.get(title=str(requested_pokemon.previous_evolution))
        pokemon_on_page.setdefault('previous_evolution',
                                   {'pokemon_id': preview_pokemon.id,
                                    'img_url': request.build_absolute_uri(f'../../media/{preview_pokemon.img}'),
                                    'title_ru': preview_pokemon.title,
                                   })
    except Pokemon.DoesNotExist:
        pass

    try:
        next_pokemon = requested_pokemon.next_evl.all()
        if next_pokemon:
            pokemon_on_page.setdefault('next_evolution',
                                       {'pokemon_id': next_pokemon[0].id,
                                        'img_url': request.build_absolute_uri(f'../../media/{next_pokemon[0].img}'),
                                        'title_ru': next_pokemon[0].title,
                                        })

    except Pokemon.DoesNotExist:
        pass

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entitys = PokemonEntity.objects.filter(pokemon=requested_pokemon, appeared_at__lte=localtime,
                                                   disappeared_at__gt=localtime)

    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            filepath
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })

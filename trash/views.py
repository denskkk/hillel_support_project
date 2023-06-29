import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from random import choice, randint
from string import ascii_letters

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import path

from core.models import User


# Create your views here.
def filter_by_keys(source: dict, keys: list[str]) -> dict:
    filtered_data = {}

    for key, value in source.items():
        if key in keys:
            filtered_data[key] = value

    return filtered_data


@dataclass
class Pokemon:
    id: int
    name: str
    height: int
    weight: int
    base_experience: int

    @classmethod
    def from_raw_data(cls, raw_data: dict) -> "Pokemon":
        filtered_data = filter_by_keys(
            raw_data,
            cls.__dataclass_fields__.keys(),
        )
        return cls(**filtered_data)


# ============================================
# Simulate the CACHE
# ============================================
TTL = timedelta(seconds=5)
POKEMONS: dict[str, list[Pokemon, datetime]] = {}


def get_pokemon_from_api(name: str) -> Pokemon:
    url = settings.POKEAPI_BASE_URL + f"/{name}"
    response = requests.get(url)
    raw_data = response.json()

    return Pokemon.from_raw_data(raw_data)


def _get_pokemon(name) -> Pokemon:
    """
    Take pokemon from the cache or
    fetch it from the API and then save it to the cache.
    """

    if name in POKEMONS:
        pokemon, created_at = POKEMONS[name]

        if datetime.now() > created_at + TTL:
            del POKEMONS[name]
            return _get_pokemon(name)
    else:
        pokemon: Pokemon = get_pokemon_from_api(name)
        POKEMONS[name] = [pokemon, datetime.now()]

    return pokemon


def get_pokemon(request, name: str):
    pokemon: Pokemon = _get_pokemon(name)
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(asdict(pokemon)),
    )


def get_all_pokemons(request):
    pokemons = [pokemon for pokemon, _ in POKEMONS.values()]
    return JsonResponse([asdict(pokemon) for pokemon in pokemons], safe=False)


def delete_pokemon(request, name: str):
    if name in POKEMONS:
        del POKEMONS[name]
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def get_pokemon_for_mobile(request, name: str):
    pokemon: Pokemon = _get_pokemon(name)
    result = filter_by_keys(
        asdict(pokemon),
        ["id", "name", "base_experience"],
    )

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )


# Roles are hardcoded instead of beeing used in the database

ROLES = {
    "ADMIN": 1,
    "MANAGER": 2,
    "USER": 3,
}


def _get_random_sting(size: int = 5) -> str:
    return "".join([choice(ascii_letters) for _ in range(size)])


def create_random_user(request):
    email_prefix = _get_random_sting(size=randint(5, 8))
    email_affix = _get_random_sting(size=randint(2, 5))
    email = "".join((email_prefix, "@", email_affix, "com"))

    user = User.objects.create(
        username=_get_random_sting(size=randint(5, 10)),
        email=email,
        first_name=_get_random_sting(size=randint(5, 10)),
        last_name=_get_random_sting(randint(5, 10)),
        password=_get_random_sting(randint(10, 20)),
        role=ROLES["USER"],
    )

    result = {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "role": user.role,
    }

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )


urlpatterns = [
    path("api/pokemon/<str:name>/", get_pokemon),
    path("api/pokemon/", get_all_pokemons),
    path("api/pokemon/<str:name>/", delete_pokemon),
    path("api/pokemon/mobile/<str:name>/", get_pokemon_for_mobile),
    path("create-random-user", create_random_user),
]

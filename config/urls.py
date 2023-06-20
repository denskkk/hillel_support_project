from django.contrib import admin
from django.urls import path

from core.views import (create_random_user, delete_pokemon, get_all_pokemons,
                        get_pokemon, get_pokemon_for_mobile)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pokemon/<str:name>/", get_pokemon),
    path("api/pokemon/", get_all_pokemons),
    path("api/pokemon/<str:name>/", delete_pokemon),
    path("api/pokemon/mobile/<str:name>/", get_pokemon_for_mobile),
    path("create-random-user", create_random_user),
]

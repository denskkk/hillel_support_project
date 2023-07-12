# def filter_by_keys(source: dict, keys: list[str]) -> dict:
#     filtered_data = {}
#     for key, value in source.items():
#         if key in keys:
#             filtered_data[key] = value
#     return filtered_data
#
#
# @dataclass
# class Pokemon:
#     id: int
#     name: str
#     height: int
#     weight: int
#     base_experience: int
#
#     @classmethod
#     def from_raw_data(cls, raw_data: dict) -> "Pokemon":
#         filtered_data = filter_by_keys(
#             raw_data,
#             cls.__dataclass_fields__.keys(),
#         )
#         return cls(**filtered_data)
#
#
# # ============================================
# # Simulate the CACHE
# # ============================================
# TTL = timedelta(seconds=5)
# POKEMONS: dict[str, list[Pokemon, datetime]] = {}
#
#
# def get_pokemon_from_api(name: str) -> Pokemon:
#     url = settings.POKEAPI_BASE_URL + f"/{name}"
#     response = requests.get(url)
#     raw_data = response.json()
#
#     return Pokemon.from_raw_data(raw_data)
#
#
# def _get_pokemon(name) -> Pokemon:
#     """
#     Take pokemon from the cache or
#     fetch it from the API and then save it to the cache.
#     """
#
#     if name in POKEMONS:
#         pokemon, created_at = POKEMONS[name]
#
#         if datetime.now() > created_at + TTL:
#             del POKEMONS[name]
#             return _get_pokemon(name)
#     else:
#         pokemon: Pokemon = get_pokemon_from_api(name)
#         POKEMONS[name] = [pokemon, datetime.now()]
#
#     return pokemon
#
#
# def get_pokemon(request, name: str):
#     pokemon: Pokemon = _get_pokemon(name)
#     return HttpResponse(
#         content_type="application/json",
#         content=json.dumps(asdict(pokemon)),
#     )
#
#
# def get_pokemon_for_mobile(request, name: str):
#     pokemon: Pokemon = _get_pokemon(name)
#     result = filter_by_keys(
#         asdict(pokemon),
#         ["id", "name", "base_experience"],
#     )
#
#     return HttpResponse(
#         content_type="application/json",
#         content=json.dumps(result),
#     )
#
#
# urlpatterns = [
#     path("api/pokemon/<str:name>/", get_pokemon),
#     path("api/pokemon/mobile/<str:name>/", get_pokemon_for_mobile),
# ]

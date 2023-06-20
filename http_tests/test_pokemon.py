import requests

HOST = "http://localhost:8000"


def test_get_pokemon(name):
    url = "".join([HOST, "/api/pokemon/", name])
    response = requests.get(url)
    print(response.json())


test_get_pokemon("ditto")
test_get_pokemon("pikachu")

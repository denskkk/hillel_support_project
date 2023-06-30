from dataclasses import dataclass
from typing import Any


class Settings:
    DATABASE_DRIVER = "sqlite"


ORM_MAPPINGS = {
    "CREATE_TABLE": {
        "sqlite": "CREATE TABLE IF NOT EXIST",
        "postgres": "CREATE TABLE",
    }
}


class DataMapper:
    def __init__(self, schema: object):
        self.schema = schema

    def _connect(self):
        self._session = None  # connection

    def create_table_if_not_exist(self):
        table_name = "".join((self._schema_.__name__.lower(), +"s"))
        _query = ORM_MAPPINGS[Settings.DATABASE_DRIVER]["CREATE_TABLE"]
        query = f"{_query} {table_name}"
        self._session.exexute(query)

    def insert(self, payload: dict):
        pass


class Schema:
    def __init__(self):
        self._mapper = DataMapper(self)

    id: int

    def save(self):
        self._mapper.insert({self.username})

    def delete(self, id_: int):
        pass

    def get(self, key: str, value: Any):
        self._mapper.select(...)


@dataclass
class User(Schema):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


@dataclass
class Request(Schema):
    title: str
    text: str
    visibility: bool
    user_id: int
    manage_id: int


@dataclass
class Message(Schema):
    text: str
    user_id: int
    request_id: int


#
# john = User(
#     id=1, username="john",
#     email="john@email.com",
#     password="23423424242"
# )
#
# john.save()

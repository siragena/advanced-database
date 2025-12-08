from peewee import *

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db


class Kind(BaseModel):
    name = CharField()
    food = CharField()
    sound = CharField()


class Pet(BaseModel):
    name = CharField()
    age = IntegerField()
    owner = CharField()
    kind = ForeignKeyField(Kind, backref="pets")

def initialize(database_file: str):
    """Initialize the database and create tables if needed."""
    db.init(database_file)
    db.connect()
    db.create_tables([Kind, Pet], safe=True)

def get_pets():
    """
    Return a list of pets as dictionaries with keys:
    id, name, type, age, owner
    ('type' is the kind name)
    """
    query = (
        Pet.select(
            Pet.id,
            Pet.name,
            Pet.age,
            Pet.owner,
            Kind.name.alias("type"),
        )
        .join(Kind)
    )

    return [dict(row) for row in query.dicts()]


def get_kinds():
    """
    Return a list of kinds as dictionaries with keys:
    id, name, food, sound
    """
    query = Kind.select(Kind.id, Kind.name, Kind.food, Kind.sound)
    return [dict(row) for row in query.dicts()]


def get_pet_by_id(id: int):
    query = (
        Pet.select(
            Pet.id,
            Pet.name,
            Pet.age,
            Pet.owner,
            Kind.name.alias("type"),
        )
        .join(Kind)
        .where(Pet.id == id)
        .dicts()
    )
    return query.first()  # returns dict or None


def get_kind_by_id(id: int):
    query = (
        Kind.select(Kind.id, Kind.name, Kind.food, Kind.sound)
        .where(Kind.id == id)
        .dicts()
    )
    return query.first()

def create_pet(data: dict):
    """
    data: {"name":..., "age":..., "kind_id":..., "owner":...}
    """

    try:
        age = int(data.get("age") or 0)
    except ValueError:
        age = 0

    # Accept either "kind_id" or "kind" just in case
    kind_id = data.get("kind_id") or data.get("kind")
    if not kind_id:
        raise ValueError(f"Missing kind_id in data: {data}")

    kind = Kind.get_by_id(int(kind_id))

    Pet.create(
        name=data["name"],
        age=age,
        owner=data["owner"],
        kind=kind,
    )


def create_kind(data: dict):
    """
    data: {"name":..., "food":..., "sound":...}
    """
    Kind.create(
        name=data["name"],
        food=data["food"],
        sound=data["sound"],
    )


def update_pet(id: int, data: dict):
    """
    data from update form: name, age, type, owner
    'type' is the kind name (dog, cat, ...)
    """
    try:
        age = int(data.get("age") or 0)
    except ValueError:
        age = 0

    pet = Pet.get_by_id(id)
    pet.name = data["name"]
    pet.age = age
    pet.owner = data["owner"]

    type_name = data.get("type")
    if type_name:
        kind = Kind.get_or_none(Kind.name == type_name)
        if kind:
            pet.kind = kind

    pet.save()


def update_kind(id: int, data: dict):
    kind = Kind.get_by_id(id)
    kind.name = data["name"]
    kind.food = data["food"]
    kind.sound = data["sound"]
    kind.save()


def delete_pet(id: int):
    Pet.delete().where(Pet.id == id).execute()


def delete_kind(id: int):
    Kind.delete().where(Kind.id == id).execute()

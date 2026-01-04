from model.creature import Creature

_creatures: list[Creature] = [
    Creature(
        name="Cryptid",
        description="A creature that has the ability to see in the dark",
        country="Unknown",
        area="Unknown",
        aka="Cryptid",
    ),
    Creature(
        name="Cryptid2",
        description="A creature that has the ability to see in the dark2",
        country="Unknown2",
        area="Unknown2",
        aka="Cryptid2",
    ),
    Creature(
        name="Cryptid3",
        description="A creature that has the ability to see in the dark3",
        country="Unknown3",
        area="Unknown3",
        aka="Cryptid3",
    ),
]


def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(
        name=name, description=description, country=country, area=area, aka=aka
    )


def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Creature:
    for creature in _creatures:
        if creature.name == name:
            return creature
    return None


def get_all() -> list[Creature]:
    return _creatures


def create(creature: Creature) -> Creature:
    _creatures.append(creature)
    return creature


def modify(name: str, creature: Creature) -> Creature:
    for i, c in enumerate(_creatures):
        if c.name == name:
            _creatures[i] = creature
            return creature
    return None


def delete(name: str) -> None:
    for i, creature in enumerate(_creatures):
        if creature.name == name:
            del _creatures[i]
            return

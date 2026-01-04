from model.creature import Creature
from data.db_init import cursor, IntegrityError
from error import Missing, Duplicate

cursor.execute("""create table if not exists creature(
               name text primary key,
               description text,
               country text,
               area text,
               aka text
               )""")


def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(
        name=name, description=description, country=country, area=area, aka=aka
    )


def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Creature:
    qry = "select * from creature where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"Creature {name} not found")


def get_all() -> list[Creature]:
    qry = "select * from creature"
    cursor.execute(qry)
    rows = list(cursor.fetchall())
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    qry = "insert into creature values (:name, :description, :country, :area, :aka)"
    params = model_to_dict(creature)
    try:
        cursor.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Creature {creature.name} already exists")
    return get_one(creature.name)


def modify(name: str, creature: Creature) -> Creature:
    if not (name and creature):
        raise Missing(f"Creature {name} not found")
    qry = """update creature
             set country=:country,
                 name=:name,
                 description=:description,
                 area=:area,
                 aka=:aka
             where name=:name_original
                 """
    params = model_to_dict(creature)
    params["name_original"] = name
    cursor.execute(qry, params)
    if cursor.rowcount == 1:
        return get_one(creature.name)
    else:
        raise Missing(f"Creature {name} not found")


def delete(name: str) -> None:
    qry = "delete from creature where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    if cursor.rowcount != 1:
        raise Missing(f"Creature {name} not found")

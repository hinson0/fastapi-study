from model.explorer import Explorer
from .db_init import cursor, IntegrityError
from error import Missing, Duplicate

cursor.execute("""create table if not exists explorer(
               name text primary key,
               description text,
               country text
               )""")


def row_to_model(row: tuple) -> Explorer:
    name, description, country = row
    return Explorer(name=name, description=description, country=country)


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump()


def get_one(name: str) -> Explorer:
    qry = "select * from explorer where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"explorer {name} not found")


def get_all() -> list[Explorer]:
    qry = "select * from explorer"
    cursor.execute(qry)
    rows = list(cursor.fetchall())
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    qry = "insert into explorer values (:name, :description, :country)"
    params = model_to_dict(explorer)
    try:
        cursor.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Explorer {explorer.name} already exists.")
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer):
        return None
    qry = """update explorer
             set country=:country,
                 name=:name,
                 description=:description
             where name=:name_original
                 """
    params = model_to_dict(explorer)
    params["name_original"] = name
    cursor.execute(qry, params)
    if cursor.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(f"Explorer {name} not found")


def delete(name: str):
    qry = "delete from explorer where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    if cursor.rowcount != 1:
        raise Missing(f"Explorer {name} not found.")

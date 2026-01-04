from model.user import User
from .db_init import cursor, IntegrityError
from error import Missing, Duplicate

cursor.execute("""create table if not exists user(
               name text primary key,
               hash text
               )""")

cursor.execute("""create table if not exists xuser(
               name text primary key,
               hash text
               )""")


def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> dict:
    return user.model_dump()


def get_one(name: str, table: str = "user") -> User:
    qry = f"select * from {table} where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()

    if row:
        return row_to_model(row)
    else:
        raise Missing(f"User {name} not found")


def get_all(table: str = "user") -> list[User]:
    qry = f"select * from {table}"
    cursor.execute(qry)
    rows = list(cursor.fetchall())
    return [row_to_model(row) for row in rows]


def create(user: User, table: str = "user") -> User:
    qry = f"insert into {table} values (:name, :hash)"
    params = model_to_dict(user)
    try:
        cursor.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"User {user.name} already exists")
    return get_one(user.name, table)


def modify(name: str, user: User, table: str = "user") -> User:
    qry = f"""update {table}
             set name=:name,
                 hash=:hash
             where name=:name_original"""
    params = model_to_dict(user)
    params["name_original"] = name
    cursor.execute(qry, params)
    if cursor.rowcount == 1:
        return get_one(user.name, table)
    else:
        raise Missing(f"User {name} not found")


def delete(name: str, table: str = "user") -> None:
    qry = f"delete from {table} where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    if cursor.rowcount == 0:
        raise Missing(f"User {name} not found")
    create(get_one(name, table), table="xuser")

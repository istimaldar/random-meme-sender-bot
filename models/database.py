from pathlib import Path

from pony.orm import Database, PrimaryKey, Required

db = Database()


class Image(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True, index=True)
    file_id = Required(str)


def init_database(filename: str):
    file_path = str(Path(filename).absolute())
    db.bind(provider='sqlite', filename=file_path, create_db=True)
    db.generate_mapping(create_tables=True)

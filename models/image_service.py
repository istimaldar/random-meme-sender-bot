from typing import List

from pony.orm import db_session, commit, select, delete

from models.database import Image


class ImageService:
    @db_session
    def create(self, name: str, file_id: str) -> None:
        Image(name=name, file_id=file_id)
        commit()

    @db_session
    def read_all(self) -> List[Image]:
        # noinspection PyTypeChecker
        return list(select(image for image in Image))

    @db_session
    def read_by_id(self, _id: int) -> Image:
        # noinspection PyTypeChecker
        return select(image for image in Image if image.id == _id).first()

    @db_session
    def read_by_name(self, name: str) -> Image:
        # noinspection PyTypeChecker
        return select(image for image in Image if image.name == name).first()

    @db_session
    def delete(self, _id: int):
        # noinspection PyTypeChecker
        delete(image for image in Image if image.id == _id)
        commit()

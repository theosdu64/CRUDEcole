from typing import Optional, List

from ecole.models.teacher import Teacher
from ecole.daos.dao import Dao
from dataclasses import dataclass

@dataclass
class TeacherDAO(Dao[Teacher]):

    def create(self, teacher: Teacher) -> None:
        raise NotImplementedError()

    def read(self, id_entity: int) -> Optional[Teacher]:
        raise NotImplementedError()

    def read_all(self) -> List[Teacher]:
        with Dao.connection.cursor() as cursor:
            sql = """SELECT p.first_name,p.last_name 
                     FROM teacher t
                     INNER JOIN person p ON t.id_person = p.id_person"""
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                return results
            return None

    def update(self, id_entity: int, teacher: Teacher) -> None:
        raise NotImplementedError()

    def update(self, teacher: Teacher) -> None:
        raise NotImplementedError()

    def delete(self, teacher: Teacher) -> None:
        raise NotImplementedError()
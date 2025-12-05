from typing import Optional, List

from ecole.daos.address_dao import AddressDao
from ecole.models import student
from ecole.models.teacher import Teacher
from ecole.daos.dao import Dao
from dataclasses import dataclass

@dataclass
class TeacherDAO(Dao[Teacher]):

    def create(self, teacher: Teacher) -> int:
        dao_address = AddressDao()
        id_address = dao_address.create(teacher.address)

        with Dao.connection.cursor() as cursor:
            sql_person = """
                INSERT INTO person (first_name, last_name, age, id_address)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_person, (
                teacher.first_name,
                teacher.last_name,
                teacher.age,
                id_address
            ))
            id_person = cursor.lastrowid

        with Dao.connection.cursor() as cursor:
            sql_teacher = """
                INSERT INTO teacher (id_person, hiring_date)
                VALUES (%s, %s)
            """
            cursor.execute(sql_teacher, (
                id_person,
                teacher.hiring_date,
            ))
            Dao.connection.commit()

            id_teacher = cursor.lastrowid

        teacher.id = id_teacher

        return id_teacher


    def read(self, id_entity: int) -> Optional[Teacher]:
        with Dao.connection.cursor() as cursor:
            sql = """SELECT p.first_name,p.last_name 
                     FROM teacher t
                     INNER JOIN person p ON t.id_person = p.id_person
                     WHERE t.id_person = %s
                     """
            cursor.execute(sql, id_entity)
            results = cursor.fetchone()
            if results:
                return results
            return None

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


    def delete(self, teacher: Teacher) -> None:
        raise NotImplementedError()
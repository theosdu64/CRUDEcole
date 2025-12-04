from multiprocessing.connection import address_type

from ecole.models.student import Student
from ecole.daos.address_dao import AddressDao
from ecole.daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class StudentDAO(Dao[Student]):

    def create(self, student: Student) -> int:
        dao_address = AddressDao()
        id_address = dao_address.create(student.address)
        with Dao.connection.cursor() as cursor:
            sql_person = """
                INSERT INTO person (first_name, last_name, age, id_address)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_person, (
                student.first_name,
                student.last_name,
                student.age,
                id_address
            ))
            id_person = cursor.lastrowid

        with Dao.connection.cursor() as cursor:
            sql_student = "INSERT INTO student (id_person) VALUES (%s)"
            cursor.execute(sql_student, (id_person,))
            Dao.connection.commit()
            return cursor.lastrowid

    def read(self, id_student: int) -> Optional[Student]:
        with Dao.connection.cursor() as cursor:
            sql = """
               SELECT 
                s.student_nbr,
                p.first_name,
                p.last_name,
                p.age,
                a.street,
                a.city,
                a.postal_code
                FROM student AS s
                INNER JOIN person AS p
                    ON p.id_person = s.id_person
                INNER JOIN address AS a
                    ON a.id_address = p.id_address
                WHERE s.student_nbr =  %s;
            """
            cursor.execute(sql, (id_student,))
            row = cursor.fetchone()
            if row:
                return row
            return None

    def read_all(self) -> List[Student]:
        print("read_all")
        with Dao.connection.cursor() as cursor:
            sql = """
               SELECT 
                s.student_nbr,
                p.first_name,
                p.last_name,
                p.age,
                a.street,
                a.city,
                a.postal_code
                FROM student AS s
                INNER JOIN person AS p
                    ON p.id_person = s.id_person
                INNER JOIN address AS a
                    ON a.id_address = p.id_address
                """
            cursor.execute(sql)
            row = cursor.fetchall()
            if row:
                return row
            return None

    def update(self, student_nbr, obj: Student) -> bool:
        adress_dao = AddressDao()
        print("update", obj)
        try:
            with Dao.connection.cursor() as cursor:
                sql_student = """SELECT id_person FROM student WHERE student_nbr = %s"""
                cursor.execute(sql_student, (student_nbr,))
                result = cursor.fetchone()

                if not result:
                    print("student non trouvé")
                    return False

                id_person = result["id_person"]

                sql_person_adress_id = """SELECT id_address FROM person WHERE id_person = %s"""
                cursor.execute(sql_person_adress_id, (id_person,))
                result_address = cursor.fetchone()

                if not result_address:
                    print("Adresse non trouvée")
                    return False

                id_address = result_address["id_address"]

                sql_update_person = """
                    UPDATE person 
                    SET first_name = %s, last_name = %s, age = %s 
                    WHERE id_person = %s
                """
                cursor.execute(sql_update_person, (
                    obj.first_name,
                    obj.last_name,
                    obj.age,
                    id_person
                ))

                adress_dao.update(id_address, obj.address)

            Dao.connection.commit()
            print(f"{student_nbr} mis a jour")
            return True

        except Exception as e:
            Dao.connection.rollback()
            print(f"Erreur : {e}")
            return False

    def delete(self, id_student: int) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql_student = """SELECT id_person FROM student WHERE student_nbr = %s"""
                cursor.execute(sql_student, (id_student,))
                row = cursor.fetchone()

                if not row:
                    print("student non trouvé")
                    return False

                id_person = row["id_person"]

                sql_get_person_id_address = """SELECT id_address FROM person WHERE id_person = %s"""
                cursor.execute(sql_get_person_id_address, (id_person,))
                row = cursor.fetchone()

                if not row:
                    print("Adresse non trouvée")
                    return False

                id_address = row["id_address"]

                sql_delete_student = """DELETE FROM student WHERE student_nbr = %s"""
                cursor.execute(sql_delete_student, (id_student,))

                sql_delete_person = """DELETE FROM person WHERE id_person = %s"""
                cursor.execute(sql_delete_person, (id_person,))

                sql_delete_address = """DELETE FROM address WHERE id_address = %s"""
                cursor.execute(sql_delete_address, (id_address,))

            Dao.connection.commit()
            print("Étudiant supprimé")
            return True

        except Exception as e:
            Dao.connection.rollback()
            print(f"Erreur : {e}")
            return False

    def get_student_courses(self, student_id: int) -> list:
        dao_student = StudentDAO()
        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT c.name AS course_name, p.first_name AS teacher_name, p.last_name AS teacher_lastname
                from takes t
                INNER JOIN course c ON t.id_course = c.id_course
                INNER JOIN teacher te ON  te.id_teacher = c.id_teacher
                INNER JOIN person p ON te.id_person = p.id_person
                WHERE student_nbr =%s;
            """
            cursor.execute(sql, (student_id,))
            rows = cursor.fetchall()
            courses = [
                {
                    "course": r["course_name"],
                    "teacher": f"{r['teacher_name']} {r['teacher_lastname']}"
                }
                for r in rows
            ] if rows else []

            for c in courses:
                print(f"Cours de : {c['course']}\nProf: {c['teacher']}\n")

        return courses



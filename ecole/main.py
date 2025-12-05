from datetime import date

from ecole.daos.student_dao import StudentDAO
from ecole.daos.teacher_dao import TeacherDAO
from ecole.models.address import Address
from ecole.models.student import Student
from ecole.models.teacher import Teacher


def test_student_dao():
    dao_student = StudentDAO()

    new_adress = Address(
        street="12 rue de dax",
        city="Dax",
        postal_code=40000
    )

    student = Student(
        first_name="Jonathan",
        last_name="Leouf",
        age=18
    )

    student.address = new_adress

    student_id = dao_student.create(student)
    print(f"student créé : {student_id}")

def get_student_dao():
    dao_student = StudentDAO()
    print(dao_student.read_all())
    print(dao_student.read(3))

def update_address_dao():
    dao_student = StudentDAO()
    print("Avant modif")
    print(dao_student.read(3))

    address = Address(
        street="1 rue du test",
        postal_code=20010,
        city="Pau",
    )
    updated_student = Student(
        first_name="Jean-Test",
        last_name="Test",
        age=25
    )
    updated_student.address = address

    test = dao_student.update(3, updated_student)

    if test:
        print("Apres modif")
        print(dao_student.read(3))

def delete_student_dao():
    dao_student = StudentDAO()
    dao_student.delete(4)

def get_student_courses_dao():
    dao_student = StudentDAO()
    return dao_student.get_student_courses(2)

def get_teachers_dao():
    dao_teacher = TeacherDAO()
    return dao_teacher.read_all()

def get_teacher_by_id_dao():
    dao_teacher = TeacherDAO()
    return dao_teacher.read(4)

def create_teacher_dao():
        print("teacher avant creation")
        print(get_teachers_dao())

        address = Address(
            street="29 rue du bourg",
            city="Nancy",
            postal_code=10000
        )

        teacher = Teacher(
            first_name="Jean",
            last_name="Mathieu",
            age=55,
            hiring_date=date(2020, 9, 2)
        )
        teacher.address = address

        dao = TeacherDAO()
        new_id = dao.create(teacher)

        print(f"Prof cree id : {new_id}")
        print(teacher)
        print("teacher apres creation")
        print(get_teachers_dao())

if __name__ == "__main__":
    print(get_teacher_by_id_dao())

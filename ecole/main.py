from ecole.daos.student_dao import StudentDAO
from ecole.models.address import Address
from ecole.models.student import Student


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
    dao_student.get_student_courses(2)

if __name__ == "__main__":
    print(get_student_courses_dao())

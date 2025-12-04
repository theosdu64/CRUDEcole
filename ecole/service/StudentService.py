class StudentService:
    def __init__(self, studentDAO, personDAO):
        self.studentDAO = studentDAO
        self.personDAO = personDAO

    def get_full_student(self, id_student: int):
        student = self.studentDAO.read(id_student)
        if not student:
            return None

        student["person"] = self.personDAO.read(student["id_person"])
        return student

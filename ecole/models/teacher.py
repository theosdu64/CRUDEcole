from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date
from .person import Person
from .course import Course

@dataclass
class Teacher(Person):
    hiring_date: date
    id: Optional[int] = field(default=None)
    courses_taught: List[Course] = field(default_factory=list, init=False)

    def add_course(self, course: Course) -> None:
        course.teacher = self

    def __str__(self) -> str:
        person_str = super().__str__()
        return f"{person_str}, arrivé(e) le {self.hiring_date}"

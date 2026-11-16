class Student:
    def __init__(self, name):
        self.name = name
        self._grades = {}  # предмет -> список оценок

    def add_grade(self, subject, grade):
        if type(grade) is not int or not (2 <= grade <= 5):
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        self._grades.setdefault(subject, []).append(grade)

    def average(self, subject=None):
        if subject is None:
            all_grades = [g for grades in self._grades.values() for g in grades]
            return sum(all_grades) / len(all_grades) if all_grades else 0

        if subject not in self._grades or not self._grades[subject]:
            raise KeyError(f"Нет оценок по предмету {subject!r}")
        subj_grades = self._grades[subject]
        return sum(subj_grades) / len(subj_grades)

    def subjects(self):
        return sorted(self._grades.keys())

    def debts(self):
        return sorted(
            subj for subj, grades in self._grades.items()
            if sum(grades) / len(grades) < 3
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average() < other.average()

    def __repr__(self):
        return f"Student({self.name!r}, {self.average():.2f})"


class Group:
    def __init__(self, name):
        self.name = name
        self._students = {}  # имя студента -> объект Student

    def add(self, student):
        if not isinstance(student, Student):
            raise TypeError("В группу можно добавлять только объекты Student")
        if student.name in self._students:
            raise ValueError(f"Студент с именем {student.name!r} уже есть в группе")
        self._students[student.name] = student

    def __len__(self):
        return len(self._students)

    def __contains__(self, name):
        return name in self._students

    def ranking(self):
        return sorted(
            self._students.values(),
            key=lambda s: (-s.average(), s.name)
        )

    def with_debts(self):
        return sorted(
            student.name for student in self._students.values()
            if student.debts()
        )


if __name__ == "__main__":
    a = Student("Аня")
    a.add_grade("матанализ", 5)
    a.add_grade("матанализ", 4)
    a.add_grade("информатика", 5)

    b = Student("Боря")
    b.add_grade("матанализ", 2)
    b.add_grade("информатика", 4)

    print(a.average())               
    print(a.average("матанализ"))    
    print(a.subjects())              
    print(b.debts())                 
    print(b < a)                     

    try:
        a.average("физика")
    except KeyError as e:
        print(f"KeyError: {e}")

    g = Group("ИСиТ-1")
    g.add(a)
    g.add(b)
    print("Аня" in g)                
    print(g.ranking())               
    print(g.with_debts())            

    try:
        g.add(Student("Аня"))
    except ValueError as e:
        print(f"ValueError: {e}")

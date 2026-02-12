
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, major):
        super().__init__(name)
        self.major = major

student1 = Student("Aslan", "Computer Science")
print(student1.name, student1.major)

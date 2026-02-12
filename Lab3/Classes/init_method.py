
class Student:
    university = "KBTU"  

    def __init__(self, name):
        self.name = name  

student1 = Student("Aslan")
student2 = Student("Ali")

print(student1.university)
print(student2.university)

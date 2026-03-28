
class Person:
    def __init__(self, name, age):
        self.name = name   
        self.age = age        

    def greet(self):
        return f"Hi, I'm {self.name}"

person1 = Person("Aslan", 19)
print(person1.greet())

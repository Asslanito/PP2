
class Animal:
    def speak(self):
        return "Animal makes a sound"

class Dog(Animal):
    pass

dog = Dog()
print(dog.speak())


class Animal:
    def speak(self):
        return "Animal sound"

class Cat(Animal):
    def speak(self):
        return "Meow"

cat = Cat()
print(cat.speak())

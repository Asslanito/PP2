
class Father:
    def skill1(self):
        return "Driving"

class Mother:
    def skill2(self):
        return "Cooking"

class Child(Father, Mother):
    pass

child = Child()
print(child.skill1())
print(child.skill2())

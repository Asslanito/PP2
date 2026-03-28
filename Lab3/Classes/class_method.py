
class Car:
    def __init__(self, brand):
        self.brand = brand

car1 = Car("Toyota")
print(car1.brand)

car1.brand = "BMW"  
print(car1.brand)

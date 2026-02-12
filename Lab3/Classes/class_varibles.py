
class Book:
    def __init__(self, title):
        self.title = title

book1 = Book("Python Basics")
print(book1.title)

del book1.title


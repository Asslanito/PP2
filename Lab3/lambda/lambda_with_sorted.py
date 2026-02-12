
students = [
    ("Aslan", 85),
    ("Ali", 92),
    ("Dana", 78)
]

# Sort by grade
sorted_students = sorted(students, key=lambda student: student[1])

print(sorted_students)

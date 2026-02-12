def student_info(*args, **kwargs):
    """
    *args stores positional arguments as tuple
    **kwargs stores keyword arguments as dictionary
    """
    print("Courses:", args)
    print("Details:", kwargs)

student_info("Math", "Physics", name="Aslan", age=19)
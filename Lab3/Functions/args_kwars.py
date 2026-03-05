# Example 4: Passing list to function

def calculate_sum(numbers):
    """
    Takes a list of numbers and returns their sum.
    """
    total = 0
    for num in numbers:
        total += num
    return total

my_list = [1, 2, 3, 4, 5]
print("Sum:", calculate_sum(my_list))

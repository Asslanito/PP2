def string_to_number(s):
    mapping = {
        "ZER": "0",
        "ONE": "1",
        "TWO": "2",
        "THR": "3",
        "FOU": "4",
        "FIV": "5",
        "SIX": "6",
        "SEV": "7",
        "EIG": "8",
        "NIN": "9"
    }
    
    number = ""
    for i in range(0, len(s), 3):
        triplet = s[i:i+3]
        number += mapping[triplet]
    
    return int(number)


def number_to_string(n):
    mapping = {
        "0": "ZER",
        "1": "ONE",
        "2": "TWO",
        "3": "THR",
        "4": "FOU",
        "5": "FIV",
        "6": "SIX",
        "7": "SEV",
        "8": "EIG",
        "9": "NIN"
    }
    
    result = ""
    for digit in str(n):
        result += mapping[digit]
    
    return result


expression = input()

# Определяем оператор
if "+" in expression:
    left, right = expression.split("+")
    result = string_to_number(left) + string_to_number(right)
elif "-" in expression:
    left, right = expression.split("-")
    result = string_to_number(left) - string_to_number(right)
elif "*" in expression:
    left, right = expression.split("*")
    result = string_to_number(left) * string_to_number(right)

print(number_to_string(result))

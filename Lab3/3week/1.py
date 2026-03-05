a = input()

for digit in a:
    if int(digit) % 2 != 0:
        print("Not valid")
        break
else:
    print("Valid")

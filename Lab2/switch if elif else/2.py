def switch_example(option):
    switch = {
        1: "Option 1 selected",
        2: "Option 2 selected",
        3: "Option 3 selected"
    }
    return switch.get(option, "Invalid option")  # default

print(switch_example(2))  # Option 2 selected
print(switch_example(5))  # Invalid option
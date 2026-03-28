# 1.
print(re.findall(r"\d{4}", "2026 and 10"))

# 2.
print(re.findall(r"\b\w{3,5}\b", "Hi, hello there world"))

# 3.
print(re.findall(r"bo+", "bo, boo, booo, b"))
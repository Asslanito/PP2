# 1.
print(re.findall(r"python", "PYTHON is fun", re.IGNORECASE))

# 2.
multi_txt = "Hello\nWorld"
print(re.findall(r"^World", multi_txt, re.MULTILINE))
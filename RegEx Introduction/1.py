import re
# 1.
txt = "Learning Python is fun"
print(re.search("Python", txt)) 

# 2.
txt2 = "2026 starts now"
print(re.search(r"\d", txt2))
# 1. 
print(re.search(r"^Hello.*World$", "Hello Beautiful World"))

# 2.
print(re.findall(r"he.*o", "helo, hello, heyoo"))

# 3.
print(re.findall(r"apple|banana", "I like apple and banana"))
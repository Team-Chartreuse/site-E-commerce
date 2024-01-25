#!/bin/python3

n = str(input("Enter the name: ")).lower().replace('é', 'e').replace('è', 'e').replace('ê', 'e')

new_name = ""
for c in n:
    ascii_code = ord(c)
    if ascii_code < 65 or (90 < ascii_code < 97) or ascii_code > 122:
        if new_name[-1:] != "_" and len(new_name) > 0:
            new_name += "_"
    else:
        new_name += c.lower()

if new_name[-1:] == "_":
    new_name = new_name[:-1]

print(new_name)

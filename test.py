correct = [(6, 4, 4, 3, 3), (5, 3, 1, 1, 1, 1), (4, 2, 2), (2, 2, 2, 2, 2, 1), (4, 2, 1, 1, 1), (6, 3, 1, 1, 1), (2, 1), (4, 4, 1, 1, 1, 1), (5, 2, 2, 1, 1, 1), (4, 4, 3, 1, 1), (3, 3, 2, 1, 1), (5, 5, 3), (6, 6, 5, 4, 2), (5, 5, 5, 3, 1, 1), (1,), (5, 5, 5, 2, 2, 2), (3, 3, 2, 2, 1, 1), (2, 2, 2, 1), (6, 2, 2, 1, 1), (5, 2, 1, 1), (6, 1, 1, 1, 1, 1), (5, 3, 3, 2), (6, 4, 2), (6, 6, 6, 5, 2), (5, 5, 4, 4, 3, 2), (5, 4), (3, 2), (3, 1, 1), (5, 1, 1, 1, 1), (5, 5, 4, 2, 1, 1), (6, 6, 4, 3, 2), (5, 5, 4, 3, 2, 2), (3, 3, 3, 1, 1, 1), (5, 3, 2), (3, 3, 3, 2, 2), (4, 4, 2, 2, 2), (6, 6, 3, 3, 3), (6, 5), (2, 2, 2, 2, 1), (5, 5, 4, 4, 4, 3), (3, 3, 1, 1), (2, 2, 1), (6, 2, 2, 2), (6, 4, 3, 3, 2), (4, 1, 1, 1), (4, 3), (5, 5, 2, 2), (6, 3, 3)]

s = [(8, 8, 8, 6, 4), (4, 2, 2), (6, 6, 5, 5, 3, 3, 3), (6, 6, 6, 3, 3, 3, 2), (7, 7, 6, 6, 4, 2), (8, 8, 4, 3, 3), (7, 5, 5, 3, 3, 3, 1, 1), (6, 3, 1, 1, 1), (7, 4, 4, 3, 2, 2, 1, 1), (4, 4, 3, 2, 2, 2, 1, 1), (8, 5, 5, 4, 4, 4, 3), (8, 8, 6, 5, 2, 1, 1), (8, 8, 8, 7, 1, 1, 1), (7, 3, 2, 1, 1, 1), (5, 5, 5, 5, 5, 4, 1, 1), (4, 4, 3, 1, 1), (7, 5, 5, 3, 3, 2), (8, 8, 8, 8, 6), (7, 5, 4, 4, 3, 3, 1, 1), (8, 8, 6, 5, 3), (5, 5, 3), (8, 6, 6, 6, 4, 4), (8, 6, 5, 4, 1, 1, 1), (8, 6, 2), (5, 5, 5, 5, 3, 3, 2, 2), (7, 3, 1, 1, 1, 1, 1, 1), (7, 5, 3, 2), (7, 5, 5, 4), (7, 4, 2, 2, 2, 2), (6, 6, 5, 4, 4, 2, 2, 2), (7, 6), (4, 4, 3, 3, 1, 1, 1), (6, 6, 5, 3, 3, 2, 2), (7, 5, 5, 5, 3, 3), (6, 6, 4, 2, 2, 1, 1, 1), (8, 8, 7, 3, 2, 2), (7, 7, 6, 6, 5, 1, 1, 1), (5, 5, 4, 2, 2, 2, 1, 1), (7, 7, 5, 4, 2, 1, 1, 1), (8, 8, 8, 7, 3), (3, 3, 3, 2, 1, 1, 1), (8, 6, 4, 3, 3, 3), (5, 5, 5, 3, 2, 2, 2, 2), (8, 2, 2, 1, 1, 1, 1), (6, 4, 3, 1, 1, 1, 1), (8, 5, 3, 3, 3, 1, 1), (4, 4, 2, 2, 1, 1, 1, 1), (7, 4, 3), (6, 6, 6, 4, 3, 2, 1, 1), (7, 5, 5, 5, 5, 4, 2, 2), (3, 2), (5, 2, 2, 2, 2, 1, 1, 1), (8, 6, 5, 3, 3), (7, 4, 1, 1, 1), (5, 5, 4, 2, 1, 1), (7, 7, 7, 5, 5, 4), (7, 5, 4, 4, 4, 2, 1, 1), (8, 8, 8, 5, 3, 2), (4, 4, 3, 2, 2, 1, 1), (7, 7, 6, 3, 2, 1, 1, 1), (7, 4, 4, 2), (5, 3, 2), (7, 2, 2, 2, 2), (8, 8, 7, 5, 5), (8, 5, 4, 4, 4, 3, 3), (2, 2, 2, 2, 1), (7, 5, 5, 5, 4, 2, 2, 2), (7, 7, 7, 6, 5, 5, 1, 1), (6, 2, 2, 2), (4, 4, 4, 1, 1, 1, 1, 1), (3, 3, 2, 2, 2, 2, 1, 1), (4, 1, 1, 1), (7, 3, 3, 3, 2, 2), (8, 5, 4, 2), (7, 5, 2), (8, 8, 5, 1, 1), (6, 6, 5, 3, 3, 3, 2, 2), (5, 5, 5, 2, 1, 1, 1, 1), (5, 5, 5, 3, 3, 2, 1, 1), (8, 8, 3, 3, 3, 3), (6, 3, 3), (7, 7, 5, 4, 1, 1), (6, 4, 4, 3, 3), (7, 7, 3, 2, 2, 1, 1, 1), (6, 6, 3, 2, 1, 1, 1, 1), (5, 5, 5, 5, 4, 4, 3, 3), (5, 5, 1, 1, 1, 1, 1), (5, 5, 4, 3, 3, 3, 2, 2), (6, 6, 6, 4, 2, 1, 1, 1), (8, 8, 8, 6, 2, 2), (2, 1), (5, 3, 3, 3, 2, 2, 1, 1), (6, 6, 5, 5, 2, 2, 2, 2), (7, 5, 4, 4, 4, 4, 4, 3), (7, 7, 6, 4, 4, 3), (8, 8, 6, 6, 3, 2), (7, 3, 3, 2, 1, 1), (8, 4, 3, 2, 2, 2, 2), (5, 2, 2, 1, 1, 1), (8, 6, 5, 4, 3, 3), (7, 7, 7, 6, 4, 2, 1, 1), (3, 3, 2, 1, 1), (8, 8, 7, 4, 3, 2), (6, 6, 6, 3, 3, 1, 1, 1), (3, 3, 3, 3, 2, 2, 2), (1,), (7, 5, 4, 4, 4, 4, 3, 2), (7, 7, 7, 7, 7, 6, 1, 1), (8, 8, 6, 5, 2, 2), (3, 3, 2, 2, 1, 1), (8, 3, 2, 2, 2), (8, 6, 4, 4, 2, 2), (6, 6, 3, 2, 2, 2, 2), (7, 7, 7, 4, 4, 1, 1, 1), (7, 7, 6, 5, 1, 1), (6, 6, 6, 4, 4, 3, 1, 1), (8, 4, 3, 3, 3), (6, 3, 2, 1, 1, 1, 1), (3, 3, 3, 3, 1, 1, 1, 1), (6, 6, 6, 6, 4, 4, 1, 1), (7, 7, 7, 5, 2, 1, 1, 1), (6, 6, 6, 5, 2), (6, 4, 2), (8, 6, 5, 3, 2, 2), (3, 3, 2, 2, 2, 1, 1), (5, 4), (8, 6, 3, 3, 2), (8, 6, 4, 2, 2, 1, 1), (6, 6, 6, 5, 5, 5, 1, 1), (7, 4, 4, 4, 2, 2, 2, 2), (6, 6, 4, 3, 3, 3, 3, 2), (8, 6, 6, 6, 6, 3, 3), (8, 6, 4, 4, 3, 2, 2), (6, 6, 4, 3, 2), (5, 5, 2, 1, 1, 1, 1, 1), (7, 7, 6, 4, 3, 2), (6, 6, 6, 6, 5, 1, 1), (5, 5, 5, 4, 4, 3, 2, 2), (3, 3, 3, 1, 1, 1), (5, 3, 3, 3, 3, 2, 2, 2), (8, 8, 5, 2), (5, 3, 3, 1, 1, 1, 1), (3, 3, 3, 2, 2), (8, 5, 4, 4, 3, 3, 2), (6, 6, 3, 3, 3), (6, 4, 4, 2, 2, 1, 1), (7, 5, 5, 2, 2, 1, 1, 1), (5, 5, 4, 4, 2, 2, 2, 2), (5, 5, 4, 4, 4, 3), (8, 4, 4), (6, 4, 4, 4, 3, 2, 2), (5, 2, 2, 2, 1, 1, 1), (2, 2, 1), (6, 6, 6, 4, 4, 2, 2), (4, 4, 3, 3, 3, 2, 2, 2), (6, 4, 3, 3, 2), (6, 6, 4, 4, 3, 3, 1, 1), (7, 7, 5, 5, 2, 2, 1, 1), (7, 7, 3, 2, 2, 2), (7, 4, 2, 2, 2, 1, 1, 1), (8, 6, 5, 5, 4, 4, 4), (6, 6, 6, 5, 4, 2, 1, 1), (7, 5, 4, 4, 3, 2, 2, 2), (7, 5, 4, 2, 1, 1, 1, 1), (7, 5, 5, 5, 5, 5, 4, 2), (6, 6, 6, 6, 6, 4, 4), (6, 6, 4, 4, 4, 4, 3, 3), (8, 8, 2, 2, 2, 2, 2), (8, 8, 7, 6, 3), (7, 7, 7, 5, 5, 2, 1, 1), (4, 2, 1, 1, 1), (7, 7, 5, 3, 3, 3), (6, 6, 4, 3, 3, 2, 1, 1), (8, 6, 6, 4, 2, 1, 1), (8, 3, 3, 3), (7, 7, 6, 2, 2, 2, 1, 1), (8, 5, 2, 2, 2, 2), (8, 5, 5, 5, 3, 3, 3), (7, 4, 4, 4, 3, 2, 1, 1), (8, 6, 5, 5, 5, 4), (5, 5, 5, 5, 5, 3, 3, 2), (8, 4, 2, 2), (8, 8, 4, 4, 4, 1, 1), (7, 5, 4, 4, 4, 3, 2, 2), (5, 5, 5, 2, 2, 2), (8, 5, 1, 1, 1), (2, 2, 2, 1), (6, 2, 2, 1, 1), (5, 2, 1, 1), (7, 2, 1, 1, 1, 1), (7, 7, 7, 7, 5, 3), (6, 6, 4, 3, 3, 1, 1), (4, 4, 2, 1, 1, 1, 1), (4, 4, 4, 4, 3, 1, 1), (8, 8, 7, 7, 2, 1, 1), (6, 1, 1, 1, 1, 1), (8, 6, 4, 4, 4, 4, 3), (5, 3, 3, 2), (8, 1, 1, 1, 1, 1, 1, 1), (7, 5, 3, 3, 2, 2, 1, 1), (5, 5, 5, 4, 4, 4, 4, 3), (8, 6, 3, 2), (8, 8, 4, 4, 2), (8, 6, 3, 3, 3, 3, 2), (3, 1, 1), (8, 5, 2, 2, 1, 1, 1), (5, 1, 1, 1, 1), (8, 8, 5, 3, 1, 1, 1), (8, 2, 2, 2, 1, 1), (6, 6, 6, 6, 4, 3, 3), (6, 4, 4, 4, 4, 4, 3), (4, 4, 3, 3, 2, 1, 1, 1), (8, 5, 4, 3, 3, 2, 2), (4, 4, 4, 2, 2, 2, 2), (5, 5, 5, 4, 4, 4, 3, 2), (8, 7), (7, 7, 7, 5, 4, 3), (8, 5, 5, 3, 3, 3, 2), (7, 3, 3, 1, 1), (6, 6, 5, 2, 2, 2, 1, 1), (7, 5, 3, 3, 1, 1), (6, 5), (7, 5, 4, 4, 2, 1, 1, 1), (8, 6, 6, 4, 3), (6, 4, 4, 4, 4, 3, 2), (8, 3, 1, 1, 1, 1, 1), (6, 6, 6, 6, 5, 2, 1, 1), (6, 4, 1, 1, 1, 1, 1, 1), (3, 3, 1, 1), (7, 7, 6, 6, 6, 5), (8, 6, 4, 3, 1, 1, 1), (6, 6, 4, 4, 4, 3, 2, 2), (5, 5, 5, 5, 4, 3, 1, 1), (8, 8, 6, 4, 1, 1, 1), (7, 5, 3, 3, 3, 1, 1, 1), (5, 5, 5, 5, 4, 4, 4, 2), (7, 4, 4, 4, 4, 3, 1, 1), (7, 7, 7, 4, 2, 2, 1, 1), (7, 7, 7, 5, 3, 3, 1, 1), (7, 7, 6, 6, 5, 4), (7, 4, 4, 3, 1, 1), (6, 6, 6, 2, 2, 2, 2, 2), (5, 3, 1, 1, 1, 1), (6, 4, 4, 3, 1, 1, 1), (7, 7, 5, 4, 4, 2, 1, 1), (7, 5, 4, 2, 2, 2), (2, 2, 2, 2, 2, 1), (4, 4, 1, 1, 1, 1), (8, 8, 4, 4, 4, 2), (7, 7, 7, 4, 3, 3), (5, 5, 5, 4, 3, 3, 1, 1), (8, 4, 2, 1, 1, 1), (6, 6, 5, 5, 4, 4, 2), (6, 6, 5, 3, 2, 1, 1, 1), (8, 5, 5, 2, 2, 1, 1), (6, 6, 5, 4, 2), (7, 7, 5, 5, 3, 2), (5, 5, 5, 3, 1, 1), (8, 5, 5, 5, 4, 2, 2), (8, 5, 5, 4, 3, 2, 2), (8, 8, 6, 4, 4), (8, 6, 6, 4, 4, 3), (6, 6, 6, 5, 5, 3, 3), (8, 8, 6, 3, 2), (8, 6, 6, 3, 3, 1, 1), (8, 6, 5, 5, 5, 2, 2), (6, 6, 3, 3, 2, 2, 1, 1), (7, 7, 5, 3, 3, 1, 1, 1), (6, 6, 5, 4, 3, 1, 1, 1), (8, 8, 7, 7, 4), (5, 5, 5, 5, 5, 5, 4, 4), (8, 6, 6, 5, 1, 1, 1), (7, 7, 6, 5, 4, 1, 1, 1), (7, 4, 4, 3, 3, 2, 2, 2), (8, 4, 3, 3, 2, 1, 1), (5, 5, 4, 4, 3, 2), (7, 3, 2, 2), (8, 8, 5, 3, 3, 2), (8, 8, 5, 4, 2, 1, 1), (8, 6, 5, 5, 4, 3), (6, 6, 4, 4, 3, 2, 2, 2), (8, 6, 6, 6, 5), (2, 2, 2, 2, 2, 2, 2, 1), (6, 6, 4, 4, 1, 1, 1), (7, 7, 7, 6, 3, 1, 1, 1), (6, 6, 5, 5, 4, 1, 1, 1), (7, 7, 6, 4, 3, 1, 1, 1), (6, 6, 6, 5, 4, 1, 1), (6, 3, 2, 2, 1, 1, 1, 1), (4, 4, 4, 3, 2, 1, 1), (8, 6, 6, 4, 4, 4, 4), (2, 2, 2, 2, 2, 2, 1), (7, 7, 7, 7, 4, 4), (7, 7, 7, 4, 4, 2), (6, 2, 1, 1, 1, 1, 1), (7, 5, 4, 3), (5, 5, 4, 3, 2, 2), (8, 8, 5, 4, 2, 2), (8, 4, 3, 3, 2, 2), (7, 7, 7, 6, 1, 1), (4, 4, 2, 2, 2), (8, 6, 6, 5, 4), (6, 6, 3, 3, 2, 1, 1), (7, 5, 5, 5, 5, 3, 3, 3), (8, 8, 7, 6, 1, 1, 1), (6, 6, 5, 4, 3, 3, 2), (8, 6, 4, 1, 1), (8, 6, 6, 5, 3, 3), (8, 5, 4, 4, 2, 1, 1), (8, 3, 3, 2, 2, 2), (8, 8, 8, 6, 2, 1, 1), (8, 6, 3, 3, 3, 2), (7, 7, 4), (7, 1, 1, 1, 1, 1, 1), (6, 6, 5, 4, 4, 1, 1), (6, 6, 6, 4, 3, 3, 3), (7, 7, 3, 3), (4, 3), (8, 6, 5, 5, 2, 1, 1), (7, 2, 2, 1, 1, 1, 1, 1), (5, 5, 2, 2), (7, 7, 7, 7, 6, 5, 1, 1), (7, 7, 2, 2, 2, 2, 2, 2)]

for n in s:
    if n not in correct:
        print(f"Extra: {n}")
for n in correct:
    if n not in s:
        print(f"Missing: {n}")

correct.sort()
print(correct)

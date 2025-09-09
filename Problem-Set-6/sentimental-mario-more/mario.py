while True:
    try:
        n = int(input("Positive Number? "))
        if n < 1 or n > 8:
            continue
        else:
            break
    except ValueError:
        continue

n = n + 1
for row in range(1, n):
    for space in range(1, n - row):
        print(" ", end="")
    for pyramid in range(1, row + 1):
        print("#", end="")
    for barrier in range(1, 3):
        print(" ", end="")
    for right_pyramid in range(1, row + 1):
        print("#", end="")
    print()

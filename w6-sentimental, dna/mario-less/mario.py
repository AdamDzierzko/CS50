import cs50

height = cs50.get_int("Height: ")
while (height < 1 or height > 8):
    height = cs50.get_int("Height: ")
n = height + 1
while (height > 0):
    print(" " * (height - 1), end="")
    print("#" * (n - height))
    height -= 1
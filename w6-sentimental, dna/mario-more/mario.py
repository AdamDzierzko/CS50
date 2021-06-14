import cs50

while 1:                        # imput height
    height = cs50.get_int("Height: ")
    if (height >= 1 and height <= 8):
        break

n = height + 1              # free space

while (height > 0):         # write a pyramid
    print(" " * (height - 1), end="")
    print("#" * (n - height), end="")
    print("  ", end="")
    print("#" * (n - height))
    height -= 1
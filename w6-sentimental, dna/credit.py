import cs50

credit = digit = cr = nod = a = fcd = su = 0
c = nod = legal = i = 1

credit = cs50.get_int("Number: ")       # pick creditcard number
cr = credit

while (cr / 10 >= 1):           # count digts in credit card
    nod += 1
    cr = cr / 10
    c = c * 10

a = 1 if (nod % 2 == 0) else 0  # even / odd number of digits in creditcard

for i in range(1, nod + 1):     # main algorithm

    digit = int(credit / c)     # pick first digit, the biggest

    if (i == 1):                # pick first digit in creditcard number
        fcd = int(digit * 10)
    if (i == 2):                # pick second digits in creditcard number
        fcd = int(fcd + digit)

    if (i % 2 == a):            # even digit from end of creditcard number
        digit = digit * 2       # even digit multiply by 2
        if (digit >= 10):       # if digit is equal or bigger then 10
            digit = (digit % 10) + 1

        su = su + digit         # sum of even

    else:                       # odd digit from end of creditcard number
        su = su + digit         # sum of odd

    credit = credit % c         # remove first digit in creditcard number

    c = c / 10
    i += 1

legal = 1 if (su % 10 == 0) else 0      # legal by algorithm?

if (legal == 1 and (fcd == 34 or fcd == 37) and (nod == 15)):   # AMEX ?
    print("AMEX")
elif (legal == 1 and (fcd >= 51 and fcd <= 55) and (nod == 16)):    # MASTERCARD ?
    print("MASTERCARD")
elif (legal == 1 and (fcd >= 40 and fcd <= 49) and (nod == 13 or nod == 16)):  # VISA ?
    print("VISA")
else:       # so creditcard is ILLEGAL!!!
    print("INVALID")


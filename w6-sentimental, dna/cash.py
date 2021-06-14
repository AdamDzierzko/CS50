import cs50

dollars = 0.0
cents = 0
coins = 0

while 1:
    dollars = cs50.get_float("Change owned: ")
    if (dollars > 0):
        break

cents = dollars * 100       # dollars to cents

while (cents - 25 >= 0):    # count 25c
    coins += 1
    cents = cents - 25

while (cents - 10 >= 0):    # count 10c
    coins += 1
    cents = cents - 10

while (cents - 5 >= 0):     # count 5c
    coins += 1
    cents = cents - 5

while (cents - 1 >= 0):     # count 5c
    coins += 1
    cents = cents - 1

print(coins)

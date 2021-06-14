import csv
import sys

if len(sys.argv) != 3:
    print("error")
    sys.exit(1)

file_data = open(sys.argv[1], "r")      # csv
file_dna = open(sys.argv[2], "r")       # txt

x = file_dna.read()         # list x

dna_list = csv.reader(file_data, delimiter=',')

a = list(dna_list)
b = len(a[0])

number = []
name = "No match"

for i in range(1, b):           # count number of repeats

    z = x.count(a[0][i])    # liczenie
    for j in range(z):
        cc = x.find(a[0][i] * (z - j))      # search for longest number of repeats
        if (cc >= 0):
            number.append((z - j))          # append longest number of repeats
            break


for i in range(1, len(a)):                  # indentify
    if(int(a[i][1]) == number[0]):          # first STR

        for j in range(len(number)):        # rest of nuber of STRs
            if (int(a[i][j+1]) != number[j]):
                break
            if (j == len(number) - 1):      # at end write a name
                name = str(a[i][0])

print(name)
print(a[0][3] * 13)
file_data.close()
file_dna.close()
sys.exit(0)
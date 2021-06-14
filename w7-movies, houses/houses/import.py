import csv
import sys
from cs50 import SQL

if len(sys.argv) != 2:          # check start
    print("error")
    sys.exit(1)

db = SQL("sqlite:///students.db")   # open database

file_csv = open(sys.argv[1], "r")      # csv
student_data = list(csv.reader(file_csv, delimiter=','))  # list of lists with data from csv file

l = len(student_data)

for i in range(1,l):                # main loop

    aa = student_data[i][0].split(" ")      # split inner list with name, resutlt is first, middle and last name or first and last name
    l_aa = len(aa)

    if (l_aa == 3):             # if there is middle name
        f_name = aa[0]
        m_name = aa[1]
        l_name = aa[2]

    else:                       # without middle name
        f_name = aa[0]
        m_name = None
        l_name = aa[1]

    house = student_data[i][1]      # house
    birth = student_data[i][2]      # birth

    db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?,?,?,?,?)", f_name, m_name, l_name, house, birth)     # write data into student.db

# TODO

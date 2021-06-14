import csv
import sys
from cs50 import SQL

if len(sys.argv) != 2:              # check start
    print("error")
    sys.exit(1)

db = SQL("sqlite:///students.db")
house = sys.argv[1]                                                 # house name

data = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", house)     # select from db
l = len(data)

for i in range(l):

    if(data[i]["middle"] == None):                  # if middle is none
        print(data[i]["first"] + " " + data[i]["last"] + ", born " + str(data[i]["birth"]))
    else:                                           # with middle name
        print(data[i]["first"] + " " + data[i]["middle"] + " " + data[i]["last"] + ", born " + str(data[i]["birth"]))

# TODO
